import Foundation
import Vision
import AppKit
let args = CommandLine.arguments
let outDir = args[1]
for path in args.dropFirst(2) {
    guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.recognitionLanguages = ["ko-KR","en-US"]
    req.usesLanguageCorrection = false
    let h = VNImageRequestHandler(cgImage: cg, options: [:])
    try? h.perform([req])
    var lines: [String] = []
    for o in (req.results ?? []) { if let t = o.topCandidates(1).first { lines.append(t.string) } }
    let name = (path as NSString).lastPathComponent
    try? lines.joined(separator: "\n").write(toFile: outDir + "/" + name + ".txt", atomically: true, encoding: .utf8)
    print(name, lines.count)
}
