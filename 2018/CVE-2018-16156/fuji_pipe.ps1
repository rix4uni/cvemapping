param ($ComputerName = '.') 
$npipeClient = new-object System.IO.Pipes.NamedPipeClientStream($ComputerName, 'FjtwMkic_Fjicube_32', [System.IO.Pipes.PipeDirection]::InOut,
                                                                [System.IO.Pipes.PipeOptions]::None, 
                                                                [System.Security.Principal.TokenImpersonationLevel]::Impersonation)
$pipeReader = $pipeWriter = $null
try {

	$uninstall_str = 'ChangeUninstallString'
    $npipeClient.Connect()
 
    $pipeReader = new-object System.IO.StreamReader($npipeClient)
    $pipeWriter = new-object System.IO.StreamWriter($npipeClient)
    $pipeWriter.AutoFlush = $true
  
    $pipeWriter.Write($uninstall_str)
    $pipeReader.ReadLine()	
}
finally {
    $npipeClient.Dispose()
}