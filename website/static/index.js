function deleteTask(taskId) {
  console.log("Task deleted: " + taskId);
  fetch("/delete-task", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).then((_res) => {
    window.location.href = "/tasks";
  });
}

function deleteArchivedTask(archivedTaskId) {
  console.log("Task deleted: " + archivedTaskId);
  fetch("/delete-archived-task", {
    method: "POST",
    body: JSON.stringify({ archivedTaskId: archivedTaskId }),
  }).then((_res) => {
    window.location.href = "/archivedtasks";
  });
}

function markTask(taskId) {
  fetch("/mark-task", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).then((_res) => {
    window.location.href = "/tasks";
  });
}

function unMarkTask(finishedTaskId) {
  fetch("/unmark-task", {
    method: "POST",
    body: JSON.stringify({ finishedTaskId: finishedTaskId }),
  }).then((_res) => {
    window.location.href = "/tasks";
  });
}

function returnTask(archivedTaskId) {
  fetch("/return-task", {
    method: "POST",
    body: JSON.stringify({ archivedTaskId: archivedTaskId }),
  }).then((_res) => {
    window.location.href = "/archivedtasks";
  });
}
