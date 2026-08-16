#!/usr/bin/env node

import { createReadStream, statSync } from "node:fs"
import { request } from "node:https"
import { basename, resolve } from "node:path"
import { pathToFileURL } from "node:url"

function readArgs(argv) {
  const args = { dryRun: false }
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index]
    if (value === "--dry-run") args.dryRun = true
    else if (value === "--file") args.file = argv[++index]
    else if (value === "--expected-bytes") args.expectedBytes = Number(argv[++index])
    else throw new Error(`Unknown argument: ${value}`)
  }
  if (!args.file) throw new Error("--file is required")
  if (!Number.isSafeInteger(args.expectedBytes) || args.expectedBytes < 1) {
    throw new Error("--expected-bytes must be a positive integer")
  }
  return args
}

async function readStdin() {
  let input = ""
  for await (const chunk of process.stdin) input += chunk
  if (!input.trim()) throw new Error("Upload descriptor JSON is required on stdin")
  return JSON.parse(input)
}

export function validateUploadInput({ descriptor, filePath, expectedBytes, now = Date.now() }) {
  const upload = descriptor?.upload ?? descriptor
  if (!upload || upload.method !== "PUT") throw new Error("Reelsy upload method must be PUT")
  const url = new URL(upload.url)
  if (url.protocol !== "https:") throw new Error("Reelsy upload URL must use HTTPS")
  if (!Number.isSafeInteger(upload.maxBytes) || upload.maxBytes < 1) {
    throw new Error("Reelsy upload descriptor has an invalid maxBytes value")
  }
  const expiresAt = upload.expiresAt < 1_000_000_000_000
    ? upload.expiresAt * 1_000
    : upload.expiresAt
  if (!Number.isFinite(expiresAt) || expiresAt <= now + 5_000) {
    throw new Error("Reelsy upload descriptor is expired or too close to expiry")
  }
  const absolutePath = resolve(filePath)
  const file = statSync(absolutePath)
  if (!file.isFile()) throw new Error("The local media path is not a regular file")
  if (file.size !== expectedBytes) throw new Error("The local file size changed after import creation")
  if (file.size > upload.maxBytes) throw new Error("The local file exceeds the Reelsy upload limit")
  const headers = Object.fromEntries(
    Object.entries(upload.headers ?? {}).map(([key, value]) => {
      if (typeof value !== "string") throw new Error("Reelsy upload headers must contain string values")
      return [key.toLowerCase(), value]
    }),
  )
  if (!headers["content-type"]) throw new Error("Reelsy upload descriptor is missing content-type")
  return { absolutePath, byteSize: file.size, headers, url }
}

export async function uploadMedia(input) {
  await new Promise((resolveUpload, rejectUpload) => {
    const uploadRequest = request(input.url, {
      method: "PUT",
      headers: {
        ...input.headers,
        "content-length": String(input.byteSize),
      },
      timeout: 120_000,
    }, (response) => {
      response.resume()
      if (response.statusCode && response.statusCode >= 200 && response.statusCode < 300) {
        resolveUpload()
        return
      }
      rejectUpload(new Error(`Reelsy upload failed with HTTP ${response.statusCode ?? "unknown"}`))
    })
    uploadRequest.on("timeout", () => uploadRequest.destroy(new Error("Reelsy upload timed out")))
    uploadRequest.on("error", rejectUpload)
    createReadStream(input.absolutePath).on("error", rejectUpload).pipe(uploadRequest)
  })
}

async function main() {
  const args = readArgs(process.argv.slice(2))
  const descriptor = await readStdin()
  const input = validateUploadInput({
    descriptor,
    filePath: args.file,
    expectedBytes: args.expectedBytes,
  })
  if (!args.dryRun) await uploadMedia(input)
  process.stdout.write(`${JSON.stringify({
    status: args.dryRun ? "validated" : "uploaded",
    fileName: basename(input.absolutePath),
    byteSize: input.byteSize,
    contentType: input.headers["content-type"],
  })}\n`)
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) {
  main().catch((error) => {
    process.stderr.write(`${error instanceof Error ? error.message : "Media upload failed"}\n`)
    process.exitCode = 1
  })
}
