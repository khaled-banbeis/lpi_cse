const API_URL = "http://127.0.0.1:8000/students/";

const form = document.getElementById("studentForm");
const studentTable = document.getElementById("studentTable");
const message = document.getElementById("message");

const studentIdInput = document.getElementById("studentId");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const departmentInput = document.getElementById("department");
const ageInput = document.getElementById("age");

const formTitle = document.getElementById("formTitle");
const submitBtn = document.getElementById("submitBtn");
const cancelBtn = document.getElementById("cancelBtn");
const refreshBtn = document.getElementById("refreshBtn");

// Show API errors in a readable format
function getErrorMessage(data) {
    if (data.detail) {
        return typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail);
    }

    return "Something went wrong.";
}

// GET: Fetch all students
async function loadStudents() {
    refreshBtn.disabled = true;
    studentTable.replaceChildren();

    const loadingRow = document.createElement("tr");
    const loadingCell = document.createElement("td");
    loadingCell.colSpan = 6;
    loadingCell.textContent = "Loading students...";
    loadingRow.appendChild(loadingCell);
    studentTable.appendChild(loadingRow);

    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(getErrorMessage(errorData));
        }

        const students = await response.json();
        studentTable.replaceChildren();

        if (!Array.isArray(students) || students.length === 0) {
            const row = document.createElement("tr");
            const cell = document.createElement("td");

            cell.colSpan = 6;
            cell.textContent = "No students found.";
            row.appendChild(cell);
            studentTable.appendChild(row);
            return;
        }

        students.forEach(student => {
            const row = document.createElement("tr");

            // Match the field names from your SQLAlchemy model/schema
            const values = [
                student.student_id,
                student.name,
                student.email,
                student.department,
                student.age
            ];

            values.forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value ?? "";
                row.appendChild(cell);
            });

            // Edit button
            const actionsCell = document.createElement("td");

            const editBtn = document.createElement("button");
            editBtn.type = "button";
            editBtn.textContent = "Edit";
            editBtn.className = "edit";
            editBtn.addEventListener("click", () => {
                editStudent(student);
            });

            // Delete button
            const deleteBtn = document.createElement("button");
            deleteBtn.type = "button";
            deleteBtn.textContent = "Delete";
            deleteBtn.className = "delete";
            deleteBtn.addEventListener("click", () => {
                deleteStudent(student.student_id);
            });

            actionsCell.append(editBtn, deleteBtn);
            row.appendChild(actionsCell);
            studentTable.appendChild(row);
        });

    } catch (error) {
        studentTable.replaceChildren();

        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 6;
        cell.textContent = "Could not load students: " + error.message;

        row.appendChild(cell);
        studentTable.appendChild(row);

    } finally {
        refreshBtn.disabled = false;
    }
}

// Fill the form when Edit is clicked
function editStudent(student) {
    studentIdInput.value = student.student_id;
    nameInput.value = student.name ?? "";
    emailInput.value = student.email ?? "";
    departmentInput.value = student.department ?? "";
    ageInput.value = student.age ?? "";

    formTitle.textContent = "Update Student";
    submitBtn.textContent = "Update Student";
    cancelBtn.hidden = false;

    message.textContent =
        `Editing student ID: ${student.student_id}`;

    form.scrollIntoView({ behavior: "smooth" });
    nameInput.focus();
}

// Reset the form to Add mode
function resetForm() {
    form.reset();
    studentIdInput.value = "";

    formTitle.textContent = "Add New Student";
    submitBtn.textContent = "Add Student";
    cancelBtn.hidden = true;
}

cancelBtn.addEventListener("click", () => {
    resetForm();
    message.textContent = "";
});

// POST: Create a student
// PUT: Update an existing student
form.addEventListener("submit", async event => {
    event.preventDefault();

    const id = studentIdInput.value;

    const student = {
        name: nameInput.value.trim(),
        email: emailInput.value.trim(),
        department: departmentInput.value.trim(),
        age: Number(ageInput.value)
    };

    if (!student.name || !student.email || !student.department) {
        message.textContent = "Please fill in all fields.";
        return;
    }

    if (!Number.isInteger(student.age) || student.age < 1) {
        message.textContent = "Please enter a valid age.";
        return;
    }

    const url = id
        ? `${API_URL}${encodeURIComponent(id)}`
        : API_URL;

    const method = id ? "PUT" : "POST";

    submitBtn.disabled = true;
    message.textContent = id
        ? "Updating student..."
        : "Creating student...";

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(student)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(getErrorMessage(errorData));
        }

        message.textContent = id
            ? "Student updated successfully!"
            : "Student created successfully!";

        resetForm();
        await loadStudents();

    } catch (error) {
        message.textContent = "Error: " + error.message;

    } finally {
        submitBtn.disabled = false;
    }
});

// DELETE: Delete a student by ID
async function deleteStudent(id) {
    const confirmed = confirm(
        `Are you sure you want to delete student ID ${id}?`
    );

    if (!confirmed) {
        return;
    }

    message.textContent = "Deleting student...";

    try {
        const response = await fetch(
            `${API_URL}${encodeURIComponent(id)}`,
            {
                method: "DELETE"
            }
        );

        // Your controller returns HTTP 204 No Content on success.
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(getErrorMessage(errorData));
        }

        if (studentIdInput.value === String(id)) {
            resetForm();
        }

        message.textContent = "Student deleted successfully!";
        await loadStudents();

    } catch (error) {
        message.textContent = "Delete failed: " + error.message;
    }
}

// Refresh button
refreshBtn.addEventListener("click", loadStudents);

// Load data when the page opens
loadStudents();