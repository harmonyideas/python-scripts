#region Initialize Variables
# Initialize Script Variables
$num_checkboxes = 9;
$ScriptPath = Split-Path $MyInvocation.MyCommand.Path
$Logfile = $ScriptPath + "\Robocopy Logfile.log"
$InputFileName = $ScriptPath + "\AppSync.config.xml"
#endregion

#region Start Form
Function GenerateForm {
	[reflection.assembly]::loadwithpartialname("System.Windows.Forms") | Out-Null
	[reflection.assembly]::loadwithpartialname("System.Drawing") | Out-Null
	$form1 = New-Object System.Windows.Forms.Form
	$button1 = New-Object System.Windows.Forms.Button
	$outputBox = New-Object System.Windows.Forms.TextBox #creating the text box for LOG output
	$InitialFormWindowState = New-Object System.Windows.Forms.FormWindowState
	
	# Create Checkboxes
	for ($i = 1; $i -le $num_checkboxes; $i++)
	{
		New-Variable "checkBox$i" -Value (New-Object System.Windows.Forms.CheckBox)
	}
	
	#Add selection for Domain Controllers
	$dropdownBox = New-Object System.Windows.Forms.ComboBox #creating the dropdown list
	$dropdownBox.Location = New-Object System.Drawing.Size(30,230) #location of the drop down (px) in relation to the primary window's edges (length, height)
	$dropdownBox.Size = New-Object System.Drawing.Size(125,10) #the size in px of the drop down box (length, height)
	$dropdownBox.DropDownHeight = 200 #the height of the pop out selection box
	$form1.Controls.Add($dropdownBox) #activating the drop box inside the primary window
	
	#Populate DropDown
	Parse-XML $InputFileName -InformationType LOAD_DROPDOWNBOX
	
	#Set Default Value
	$dropdownBox.SelectedIndex = 9
	
	$handler_button1_Click = 
	{
	if (Test-Path $Logfile) { Clear-Content $LogFile }	
		if ($dropdownBox.SelectedItem.ToString() -eq "ALL-SERVERS") 
		{
			$target_paths = Parse-XML $InputFileName -InformationType "ALL"
			foreach ($target_server in $target_paths.netlogon_path)
			{
				for ($y=1;$y -lt $num_checkboxes; $y++) 
				{
					$IsChecked = Invoke-Expression ("`$checkBox$($y).Checked")
					if ($IsChecked)
					{	 
						$id = Invoke-Expression ("`$checkBox$($y).Text")
						$checkBoxID = Invoke-Expression("($y)")
						
						if ($id -eq "UAT")
						{
						$file_paths = Parse-XML $InputFileName -InformationType file_paths -OfficeID $id
						$targetUAT = $target_server + $file_paths.target
						Write-Progress -Activity "Synchronizing: " -status "$($file_paths.source) TO $($target_server) AND $($CheckBoxID) AND $($targetUAT)"
						CopyFolder $file_paths.source $targetUAT $file_paths.id $checkBoxID	
						}
						else
						{
						
						$file_paths = Parse-XML $InputFileName -InformationType file_paths -OfficeID $id
						Write-Progress -Activity "Synchronizing: " -status "$($file_paths.source) TO $($target_server) AND $($CheckBoxID)"
						CopyFolder $file_paths.source $target_server $file_paths.id $checkBoxID
						}
					}
				}		
			}
		}
	else
	{
		for ($y=1;$y -lt $num_checkboxes; $y++) 
		{
			$IsChecked = $null
			$IsChecked = Invoke-Expression ("`$checkBox$($y).Checked")
			if ($IsChecked)
			{	 
				$id = Invoke-Expression ("`$checkBox$($y).Text")
				$checkBoxID = Invoke-Expression("($y)")
				
				if ($id -eq "UAT")
					{
						$file_paths = Parse-XML $InputFileName -InformationType file_paths -OfficeID $id
						$target_paths = Parse-XML $InputFileName -InformationType "domain_controllers" -ServerID $dropdownBox.SelectedItem.ToString()
						$targetUAT = $target_paths.netlogon_path + $file_paths.target
						Write-Progress -Activity "Synchronizing: " -status "$($file_paths.source) TO $($target_server) AND $($CheckBoxID) AND $($target_server)"
						CopyFolder $file_paths.source $targetUAT "" $checkBoxID	
					}
					else
					{
						$file_paths = Parse-XML $InputFileName -InformationType file_paths -OfficeID $id
						$target_paths = Parse-XML $InputFileName -InformationType "domain_controllers" -ServerID $dropdownBox.SelectedItem.ToString()
						Write-Progress -Activity "Synchronizing: " -status "$($file_paths.source) TO $($target_paths.netlogon_path)"
						CopyFolder $file_paths.source $target_paths.netlogon_path $file_paths.id $checkBoxID
					}
			}
		}		
	}		#Show Log File in outputBox
			$outputBox.Text = (Get-Content $Logfile) -join "`r`n"
	}

	$OnLoadForm_StateCorrection = 
	{		
		#Correct the initial state of the form to prevent the .Net maximized form issue
		$form1.WindowState = $InitialFormWindowState
	}

#region Initialize Form Code
	#Form
	$form1.Text = "App File Sync"
	$form1.Name = "form1"
	$form1.DataBindings.DefaultDataSourceUpdateMode = 0
	$System_Drawing_Size = New-Object System.Drawing.Size
	$System_Drawing_Size.Width = 855
	$System_Drawing_Size.Height = 425
	$form1.ClientSize = $System_Drawing_Size
	$form1.FormBorderStyle = [System.Windows.Forms.FormBorderStyle]::FixedToolWindow
	
	#Labels
	$objLabel1 = New-Object System.Windows.Forms.Label
	$objLabel1.Location = New-Object System.Drawing.Size(5,30) 
	$objLabel1.Size = New-Object System.Drawing.Size(255,30) 
	$objLabel1.Text = "Step 1: `rPlease select the update source folder(s):"
	$form1.Controls.Add($objLabel1) 
	
	$objLabel2 = New-Object System.Windows.Forms.Label
	$objLabel2.Location = New-Object System.Drawing.Size(5,190) 
	$objLabel2.Size = New-Object System.Drawing.Size(170,30) 
	$objLabel2.Text = "Step 2: `rPlease select AD Server:"
	$form1.Controls.Add($objLabel2) 
	
	$objLabel3 = New-Object System.Windows.Forms.Label
	$objLabel3.Location = New-Object System.Drawing.Size(5,300) 
	$objLabel3.Size = New-Object System.Drawing.Size(160,30) 
	$objLabel3.Text = "Step 3: `rStart Synchronization:"
	$form1.Controls.Add($objLabel3) 
	
	#Buttons
	$button1.TabIndex = 9
	$button1.Name = "button1"
	$System_Drawing_Size = New-Object System.Drawing.Size
	$System_Drawing_Size.Width = 135
	$System_Drawing_Size.Height = 23
	
	$button1.Size = $System_Drawing_Size
	$button1.UseVisualStyleBackColor = $True
	$button1.Text = "Synchronize Now!"
	$System_Drawing_Point = New-Object System.Drawing.Point
	$System_Drawing_Point.X = 30
	$System_Drawing_Point.Y = 330
	$button1.Location = $System_Drawing_Point
	$button1.DataBindings.DefaultDataSourceUpdateMode = 0
	$button1.add_Click($handler_button1_Click)
	$form1.Controls.Add($button1)
	
	#OutputBox
	$outputBox.Location = New-Object System.Drawing.Size(210,65) 
	$outputBox.Size = New-Object System.Drawing.Size(625,300) 
	$outputBox.MultiLine = $True 
	$outputBox.ScrollBars = "Vertical" 
	$form1.Controls.Add($outputBox) 
	
	#CheckBoxes
	$checkBox9.UseVisualStyleBackColor = $True
	$System_Drawing_Size = New-Object System.Drawing.Size
	$System_Drawing_Size.Width = 104
	$System_Drawing_Size.Height = 24
	$checkBox9.Size = $System_Drawing_Size
	$checkBox9.TabIndex = 8
	$checkBox9.Text = "Select All"
	$System_Drawing_Point = New-Object System.Drawing.Point
	$System_Drawing_Point.X = 125
	$System_Drawing_Point.Y = 123
	$checkBox9.Location = $System_Drawing_Point
	$checkBox9.DataBindings.DefaultDataSourceUpdateMode = 0
	$checkBox9.Name = "checkBox9"
	$form1.Controls.Add($checkBox9)
	
	$checkBox8.UseVisualStyleBackColor = $True
	$System_Drawing_Size = New-Object System.Drawing.Size
	$System_Drawing_Size.Width = 104
	$System_Drawing_Size.Height = 24
	$checkBox8.Size = $System_Drawing_Size
	$checkBox8.TabIndex = 7
	$checkBox8.Text = "UAT"
	$System_Drawing_Point = New-Object System.Drawing.Point
	$System_Drawing_Point.X = 68
	$System_Drawing_Point.Y = 123
	$checkBox8.Location = $System_Drawing_Point
	$checkBox8.DataBindings.DefaultDataSourceUpdateMode = 0
	$checkBox8.Name = "checkBox8"
	$form1.Controls.Add($checkBox8)
	
	$checkBox7.UseVisualStyleBackColor = $True
	$System_Drawing_Size = New-Object System.Drawing.Size
	$System_Drawing_Size.Width = 104
	$System_Drawing_Size.Height = 24
	$checkBox7.Size = $System_Drawing_Size
	$checkBox7.TabIndex = 6
	$checkBox7.Text = "QA"
	$System_Drawing_Point = New-Object System.Drawing.Point
	$System_Drawing_Point.X = 15
	$System_Drawing_Point.Y = 123
	$checkBox7.Location = $System_Drawing_Point
	$checkBox7.DataBindings.DefaultDataSourceUpdateMode = 0
	$checkBox7.Name = "checkBox7"
	$form1.Controls.Add($checkBox7)
	
	$checkBox6.UseVisualStyleBackColor = $True
	$System_Drawing_Size = New-Object System.Drawing.Size
	$System_Drawing_Size.Width = 104
	$System_Drawing_Size.Height = 24
	$checkBox6.Size = $System_Drawing_Size
	$checkBox6.TabIndex = 5
	$checkBox6.Text = "PA"
	$System_Drawing_Point = New-Object System.Drawing.Point
	$System_Drawing_Point.X = 125
	$System_Drawing_Point.Y = 93
	$checkBox6.Location = $System_Drawing_Point
	$checkBox6.DataBindings.DefaultDataSourceUpdateMode = 0
	$checkBox6.Name = "checkBox6"
	$form1.Controls.Add($checkBox6)
	
	$checkBox5.UseVisualStyleBackColor = $True
	$System_Drawing_Size = New-Object System.Drawing.Size
	$System_Drawing_Size.Width = 104
	$System_Drawing_Size.Height = 24
	$checkBox5.Size = $System_Drawing_Size
	$checkBox5.TabIndex = 4
	$checkBox5.Text = "NY"
	$System_Drawing_Point = New-Object System.Drawing.Point
	$System_Drawing_Point.X = 68
	$System_Drawing_Point.Y = 93
	$checkBox5.Location = $System_Drawing_Point
	$checkBox5.DataBindings.DefaultDataSourceUpdateMode = 0
	$checkBox5.Name = "checkBox5"
	$form1.Controls.Add($checkBox5)
	
	$checkBox4.UseVisualStyleBackColor = $True
	$System_Drawing_Size = New-Object System.Drawing.Size
	$System_Drawing_Size.Width = 104
	$System_Drawing_Size.Height = 24
	$checkBox4.Size = $System_Drawing_Size
	$checkBox4.TabIndex = 3
	$checkBox4.Text = "FL"
	$System_Drawing_Point = New-Object System.Drawing.Point
	$System_Drawing_Point.X = 15
	$System_Drawing_Point.Y = 93
	$checkBox4.Location = $System_Drawing_Point
	$checkBox4.DataBindings.DefaultDataSourceUpdateMode = 0
	$checkBox4.Name = "checkBox4"
	$form1.Controls.Add($checkBox4)
	
	$checkBox3.UseVisualStyleBackColor = $True
	$System_Drawing_Size = New-Object System.Drawing.Size
	$System_Drawing_Size.Width = 104
	$System_Drawing_Size.Height = 24
	$checkBox3.Size = $System_Drawing_Size
	$checkBox3.TabIndex = 2
	$checkBox3.Text = "CHI"
	$System_Drawing_Point = New-Object System.Drawing.Point
	$System_Drawing_Point.X = 125
	$System_Drawing_Point.Y = 63
	$checkBox3.Location = $System_Drawing_Point
	$checkBox3.DataBindings.DefaultDataSourceUpdateMode = 0
	$checkBox3.Name = "checkBox3"
	$form1.Controls.Add($checkBox3)
	
	$checkBox2.UseVisualStyleBackColor = $True
	$System_Drawing_Size = New-Object System.Drawing.Size
	$System_Drawing_Size.Width = 104
	$System_Drawing_Size.Height = 24
	$checkBox2.Size = $System_Drawing_Size
	$checkBox2.TabIndex = 1
	$checkBox2.Text = "CA"
	$System_Drawing_Point = New-Object System.Drawing.Point
	$System_Drawing_Point.X = 68
	$System_Drawing_Point.Y = 63
	$checkBox2.Location = $System_Drawing_Point
	$checkBox2.DataBindings.DefaultDataSourceUpdateMode = 0
	$checkBox2.Name = "checkBox2"
	$form1.Controls.Add($checkBox2)
	
	$checkBox1.UseVisualStyleBackColor = $True
	$System_Drawing_Size = New-Object System.Drawing.Size
	$System_Drawing_Size.Width = 104
	$System_Drawing_Size.Height = 24
	$checkBox1.Size = $System_Drawing_Size
	$checkBox1.TabIndex = 0
	$checkBox1.Text = "NJ"
	$System_Drawing_Point = New-Object System.Drawing.Point
	$System_Drawing_Point.X = 15
	$System_Drawing_Point.Y = 63
	$checkBox1.Location = $System_Drawing_Point
	$checkBox1.DataBindings.DefaultDataSourceUpdateMode = 0
	$checkBox1.Name = "checkBox1"
	$form1.Controls.Add($checkBox1)
	
	# Add Click-Event
	$checkBox9.Add_CheckStateChanged(
	{
	if ($checkBox9.Checked) {
		for ($i = 1; $i -lt $num_checkboxes; $i++)
		{
			$command = "`$checkBox$i.Checked" + "= `$true"
			Invoke-Expression $command
		}
	} 
	else
	{
		for ($i = 1; $i -lt $num_checkboxes; $i++)
		{
		$command = "`$checkBox$i.Checked" + "= `$false"
		Invoke-Expression $command
		}
	} 
	})
	
	#Save the initial state of the form
	$InitialFormWindowState = $form1.WindowState
	
	#Init the OnLoad event to correct the initial state of the form
	$form1.add_Load($OnLoadForm_StateCorrection)
	
	#Show the Form
	$form1.ShowDialog()| Out-Null
	
	}
#End Function
#endregion
	
#region Functions

	Function CopyFolder($SourceFolder, $TargetFolder, $OfficeID, $checkBoxID)
	{
		$TargetFolder += $OfficeID
		$ConfirmationRobocopy = New-Object -ComObject wscript.shell
		#$ConfirmationPopupRobocopy = $ConfirmationRobocopy.popup("Are you sure you want to synchronize the contents of $($SourceFolder) to $($TargetFolder)?",0,"Confirm before copying",4)
	
		if ($ConfirmationPopupRobocopy -ne 7) 
		{
			Robocopy $SourceFolder $TargetFolder /E /COPY:DT /DCOPY:T /L /NP /NFL /R:0 /W:0 /XJ /A-:T /LOG+:$Logfile
			$IsFailure = (Get-Content $Logfile) -match "ERROR"
	
			if ($IsFailure) 
			{
			$command = "`$checkBox$CheckBoxID.Checked" + "= `$true"
			Invoke-Expression ($command)
			#$outputBox.Text = (Get-Content $Logfile) -join "`r`n"
			#[Windows.Forms.MessageBox]::Show(“ROBOCOPY failed trying to $($ConfirmationPopupRobocopy) synchronize the contents of $($SourceFolder) to $($TargetFolder)”, “App Updater”, [Windows.Forms.MessageBoxButtons]::OK, [Windows.Forms.MessageBoxIcon]::Information)
			}
		else
		{
			$command = "`$checkBox$CheckBoxID.Checked" + "= `$false"
			Invoke-Expression ($command)
			#$outputBox.Text = (Get-Content $Logfile) -join "`r`n"
			#[Windows.Forms.MessageBox]::Show(“ROBOCOPY has synchronized the contents of $($SourceFolder) to $($TargetFolder)”, “App Updater”, [Windows.Forms.MessageBoxButtons]::OK, [Windows.Forms.MessageBoxIcon]::Information)
		}
		}
	$outputBox.Text = "Synchronizing Directories - Please Wait... `r`n`r`nSource folder: $($SourceFolder) `r`n `r`nTarget Folder: $($TargetFolder)”
	}

Function Parse-XML()
{
	[CmdletBinding()] 
	Param 
	(
	[parameter(Mandatory=$true)] 
	[String]$InputFileName, 
	[parameter(Mandatory=$false)] 
	[ValidateSet("domain_controllers","file_paths","LOAD_DROPDOWNBOX","ALL")] 
	[String]$InformationType = "ALL",
	[parameter(Mandatory=$false)] 
	[String]$OfficeID,
	[parameter(Mandatory=$false)]
	[String]$ServerID
	) 
Begin 
{
	if (Get-ChildItem $InputFileName -ErrorAction SilentlyContinue) 
	{
		$xmlFile = [xml](Get-Content $InputFileName) 
	} 
	else 
	{
		Write-Error "Unable to find the file.Please check if the file exists and try again." -ErrorAction Stop 
	} 
} 
Process 
{
	If ($InformationType -eq "domain_controllers") 
	{
		$parseddata = $xmlFile.Configuration.domain_controllers.server | Where-Object {$_.name -eq $ServerID} #| Select-Object -Property source
		return $parseddata
	}	 
	if ($InformationType -eq "file_paths") 
	{
		$parseddata = $xmlFile.configuration.file_paths.office | Where-Object {$_.id -eq $OfficeID} #| Select-Object -Property source
		return $parseddata
	}
	if ($InformationType -eq "ALL") 
	{
		$nodes = $xmlFile.SelectNodes("//configuration/domain_controllers/server")
		return $nodes
	} 
	if ($InformationType -eq "LOAD_DROPDOWNBOX") 
	{
	$dropdownBox.Items.Add("ALL-SERVERS") | Out-Null
		foreach ($SERVER in $xmlFile.configuration.domain_controllers.server)
		{
			$dropdownBox.Items.Add($SERVER.name) | Out-Null
		}
	}	 
} 
}
#endregion

#region Start Script
#Call the Function and generate the form
GenerateForm
#endregion

