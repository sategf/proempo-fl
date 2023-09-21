function deleteTask(taskId) {
  console.log("Task deleted: " + taskId);
  fetch("/delete-task", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).then((_res) => {
    window.location.href = "/tasks";
  });
}

function deleteFinishedTask(taskId) {
  console.log("Task deleted: " + taskId);
  fetch("/delete-finished-task", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).then((_res) => {
    window.location.href = "/tasks";
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
