# Troubleshooting

Run `paper2context doctor` first.

**OCR required:** the PDF lacks a usable text layer. v0.1.0 intentionally stops instead of returning unreliable OCR text.

**Wrong section boundaries:** inspect `structure.json`; heading detection is heuristic and publisher styles vary.

**No references detected:** the document may use an unusual heading or references may be embedded in a layout the extractor cannot reliably order.
