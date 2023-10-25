$(document).ready(function () {
   // Global variables
   var gIdCounter = 0; // Counter for generating unique IDs
   var userid;

   function generateID(baseStr) {
      return (baseStr + gIdCounter++);
   }

   async function startFileTask(event) {
      event.preventDefault();

      // Get the total number of files selected by the user.
      const totalFiles = document.getElementById('files').files.length;

      // If there are any files selected, create a FormData object to send to the server.
      if (totalFiles > 0) {
         const formData = new FormData();
         formData.append('userid', userid);
         const input = document.querySelector('input[type="file"]');

         for (let index = 0; index < totalFiles; index++) {
            const file = input.files[index];

            formData.append(`file_uploads[${index}].name`, file.name);
            formData.append(`file_uploads[${index}].jobid`, generateID('filejob'));
            formData.append(`file_uploads[${index}].progressid`, generateID('progress'));
            formData.append(`file`, file);

            // Build status elements in HTML string
            const html = `
          <div class="row">
            <div id="${formData.get(`file_uploads[${index}].jobid`)}">
                   <div class="column">File: [ ${document.getElementById('files').files[index].name} ]</div>
              <div class="column"><progress id="${formData.get(`file_uploads[${index}].progressid`)}" max="100"></div>
              <div class="taskid" id="taskid">TaskID</div>
              <button type="button" class="collapsible">Show Results</button>
              <div class="result" id="result"></div> 
            </div>
          </div>
          <hr>
          `;
            // Append the row element to the #filejob element.
            $('#filejob').append(html);
         }

         // Upload the files and start the task.
         try {
            const response = await fetch('/upload', {
               method: 'POST',
               body: formData,
               processData: false,
               contentType: false,
            });

            if (response.status === 202) {
               const data = await response.json();
               if (data.taskid.length > 0) {
                  $('#status').text('File(s) uploaded successfully. Task Started...');
               } else {
                  $('#status').text('Task ID not received - please check file extension');
               }
            } else {
               $('#status').text('An unexpected error has occurred!');
            }
         } catch (error) {
            $('#status').text('An unexpected error has occurred!');
         }
      }
   }

   function updateProgress(data) {
      // Update progress bar
      const percent = Math.floor(data.current / data.total * 100);
      document.getElementById(data.progressid).value = percent;

      // Update progress
      const progressElement = $('#' + data.filejobid).find('.progressid');
      progressElement.text('Progress: [' + percent + '%]');

      // Update the status of the job.
      const statusElement = $('#' + data.filejobid).find('.taskid');
      statusElement.html('TaskID(s): ' + data.taskid);
      //statusElement.textContent = `Status: ${data.status}`;

      //Update the job to include the taskid
        const taskidElement = $('#' + data.filejobid).find('.taskid');
        taskidElement.text('TaskID: ' + data.taskid);

      // If the job is finished, show the result.
      if (data.result) {
         const resultElement = $('#' + data.filejobid).find('.result');
         resultElement.html('Result for file: ' + data.file_path + data.result);
      }
   }

   $(function () {
      $('#csv_submit').click(startFileTask);
   });

   // Setup socketio functions
   var namespace = '/events'; // change to an empty string to use the global namespace
   // the socket.io documentation recommends sending an explicit package upon connection
   // this is specially important when using the global namespace
   var socket = io.connect('http://' + location.hostname + ':' + location.port + namespace);
   socket.on('connect', function (msg) { });
   // event handler for userid.  On initial connection, the server
   // sends back a unique userid
   socket.on('userid', function (msg) {
      userid = msg.userid;
   });
   // event handler for server sent celery status
   // the data is displayed in the "FileJob" section of the page
   socket.on('celerystatus', function (msg) {
      updateProgress(msg);
   });
   // event handler for server sent general status
   // the data is displayed in the "Status" section of the page
   socket.on('status', function (msg) {
      $('#status').text(msg.status);
   });
});
