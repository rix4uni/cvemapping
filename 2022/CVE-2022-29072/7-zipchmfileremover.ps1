# This script made by Phantomiman (Sami)
if (Test-Path "C:\Program Files\7-Zip") {
  $chmFile = "C:\Program Files\7-Zip\7-zip.chm"

  if (Test-Path $chmFile) {
    Remove-Item $chmFile
  }
}
