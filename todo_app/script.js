let todos = [];
document.getElementById("todoForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const todoInput = document.getElementById("todoInput");
  const todoText = todoInput.value;
  todos.push(todoText);
  todoInput.value = "";
  renderTodos();
});
function renderTodos() {
  const todoList = document.getElementById("todoList");
  todoList.innerHTML = "";
  todos.forEach((todo, index) => {
    const li = document.createElement("li");
    li.textContent = todo;
    const editBtn = document.createElement("button");
    editBtn.textContent = "Edit";
    editBtn.onclick = function() {
      const newText = prompt("Edit your todo:", todo);
      if (newText) {
        todos[index] = newText;
        renderTodos();
      }
    };
    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.onclick = function() {
      todos.splice(index, 1);
      renderTodos();
    };
    li.appendChild(editBtn);
    li.appendChild(deleteBtn);
    todoList.appendChild(li);
  });
}
