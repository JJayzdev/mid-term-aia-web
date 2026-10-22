param([string]$InputDirectory,[string]$OutputPath)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime] | Out-Null
[Windows.Storage.Streams.IRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime] | Out-Null
[Windows.Storage.Streams.InMemoryRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime] | Out-Null
[Windows.Storage.Streams.DataWriter,Windows.Storage.Streams,ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics.Imaging,ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.SoftwareBitmap,Windows.Graphics.Imaging,ContentType=WindowsRuntime] | Out-Null
function Await($Operation,$ResultType) {
 $method=[System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {$_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'} | Select-Object -First 1
 $task=$method.MakeGenericMethod($ResultType).Invoke($null,@($Operation)); $task.Wait(); $task.Result
}
$engine=[Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$results=@()
foreach($image in (Get-ChildItem -LiteralPath $InputDirectory -Filter '*.png' | Sort-Object Name)) {
 try {
  $stream=New-Object Windows.Storage.Streams.InMemoryRandomAccessStream
  $writer=New-Object Windows.Storage.Streams.DataWriter($stream.GetOutputStreamAt(0))
  $writer.WriteBytes([System.IO.File]::ReadAllBytes($image.FullName))
  $stored=Await ($writer.StoreAsync()) ([uint32]);$writer.DetachStream();$writer.Dispose();$stream.Seek(0)
  $decoder=Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
  $bitmap=Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
  $result=Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
  $results+=@{page=[int]$image.BaseName;text=$result.Text;lines=@($result.Lines | ForEach-Object {$_.Text});method='Windows.Media.Ocr/en-US';error=$null}
  $bitmap.Dispose();$stream.Dispose()
 } catch { $results+=@{page=[int]$image.BaseName;text='';method='Windows.Media.Ocr/en-US';error=$_.Exception.ToString()} }
}
ConvertTo-Json -InputObject @($results) -Depth 5 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
