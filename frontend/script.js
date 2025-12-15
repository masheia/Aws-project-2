// API Gateway endpoint
const API_BASE_URL = 'https://pjjf6u13f8.execute-api.us-east-1.amazonaws.com/prod';

// User role management
let userRole = null;
let studentId = null;
let userName = null;

// Check authentication on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    userRole = sessionStorage.getItem('userRole');
    studentId = sessionStorage.getItem('studentId');
    userName = sessionStorage.getItem('userName');
    
    if (!userRole) {
        // Not logged in, redirect to login
        window.location.href = 'login.html';
        return;
    }
    
    // Check if new user (just signed up)
    const isNewUser = sessionStorage.getItem('isNewUser') === 'true';
    
    // Update UI based on role
    updateUIForRole();
    
    // Show user info
    const userInfoEl = document.getElementById('userInfo');
    if (userInfoEl) {
        const roleDisplay = userRole === 'admin' ? 'Admin' : 'Student';
        userInfoEl.textContent = `${userName || studentId} (${roleDisplay})`;
    }
    
    // Initialize date fields
    const today = new Date().toISOString().split('T')[0];
    const attendanceDateEl = document.getElementById('attendanceDate');
    const filterDateEl = document.getElementById('filterDate');
    if (attendanceDateEl) attendanceDateEl.value = today;
    if (filterDateEl) filterDateEl.value = today;
    
    // Update labels and buttons based on role
    const uploadLabel = document.getElementById('uploadLabel');
    if (uploadLabel) {
        if (userRole === 'student') {
            uploadLabel.textContent = 'Upload Your Photo:';
        } else {
            uploadLabel.textContent = 'Upload Attendance Photo:';
        }
    }
    const attendanceButton = document.getElementById('attendanceButton');
    if (attendanceButton) {
        if (userRole === 'student') {
            attendanceButton.textContent = 'Mark My Attendance';
        } else {
            attendanceButton.textContent = 'Process Attendance';
        }
    }
    
    // Show welcome message for new users
    if (isNewUser && userRole === 'student') {
        const welcomeMsg = document.createElement('div');
        welcomeMsg.className = 'result success';
        welcomeMsg.style.margin = '20px 0';
        welcomeMsg.textContent = '✅ Welcome! Your account has been created and your face is registered. You can now mark your attendance!';
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(welcomeMsg, container.querySelector('.tabs'));
        }
        // Clear the flag
        sessionStorage.removeItem('isNewUser');
    }
    
    // Load attendance (only if on dashboard tab)
    if (userRole === 'admin' || document.getElementById('dashboard').classList.contains('active')) {
        loadAttendance();
    }
});

function updateUIForRole() {
    if (userRole === 'admin') {
        // Show admin-only tabs
        document.querySelectorAll('.admin-only').forEach(el => {
            el.style.display = 'block';
        });
        // Hide student-only tabs
        document.querySelectorAll('.student-only').forEach(el => {
            el.style.display = 'none';
        });
        // Update titles
        const registerTitle = document.getElementById('registerTitle');
        if (registerTitle) registerTitle.textContent = 'Register New Student';
        const attendanceTitle = document.getElementById('attendanceTitle');
        if (attendanceTitle) attendanceTitle.textContent = 'Mark Attendance';
        const dashboardTitle = document.getElementById('dashboardTitle');
        if (dashboardTitle) dashboardTitle.textContent = 'Attendance Dashboard (All Records)';
        // Show student ID and name fields for admin
        const studentIdGroup = document.getElementById('studentIdGroup');
        const studentNameGroup = document.getElementById('studentNameGroup');
        if (studentIdGroup) studentIdGroup.style.display = 'block';
        if (studentNameGroup) studentNameGroup.style.display = 'block';
        // Update button text
        const registerButton = document.getElementById('registerButton');
        if (registerButton) {
            registerButton.textContent = 'Register Student';
        }
    } else {
        // Show student-only tabs (only attendance and history, no register)
        document.querySelectorAll('.student-only').forEach(el => {
            el.style.display = 'block';
        });
        // Hide admin-only tabs
        document.querySelectorAll('.admin-only').forEach(el => {
            el.style.display = 'none';
        });
        // Hide register tab for students (face upload happens during signup)
        const registerTab = document.getElementById('register');
        if (registerTab) registerTab.style.display = 'none';
        
        // Update titles
        const attendanceTitle = document.getElementById('attendanceTitle');
        if (attendanceTitle) attendanceTitle.textContent = 'Mark My Attendance';
        const dashboardTitle = document.getElementById('dashboardTitle');
        if (dashboardTitle) dashboardTitle.textContent = 'My Attendance History';
        
        // Show attendance tab by default for students
        const attendanceBtn = document.querySelector('.student-only[onclick*="attendance"]');
        if (attendanceBtn) {
            showTab('attendance', attendanceBtn);
        }
    }
}

function logout() {
    sessionStorage.clear();
    window.location.href = 'login.html';
}

// Tab switching
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Update button state
    event.target.classList.add('active');
}


// Preview image
function previewImage(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    
    if (input && preview && input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Convert image to base64
function getBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

// Register face
async function registerFace() {
    const studentIdInput = document.getElementById('studentId');
    const studentNameInput = document.getElementById('studentName');
    const imageFileInput = document.getElementById('registerImage');
    const resultDiv = document.getElementById('registerResult');
    
    if (!imageFileInput || !resultDiv) return;
    
    // For students, use logged-in student ID and name
    let regStudentId, regStudentName;
    if (userRole === 'student') {
        regStudentId = studentId; // Use logged-in student ID
        regStudentName = userName || studentId; // Use logged-in name or ID
    } else {
        // For admin, use form values
        if (!studentIdInput || !studentNameInput) return;
        regStudentId = studentIdInput.value.trim();
        regStudentName = studentNameInput.value.trim();
    }
    
    const imageFile = imageFileInput.files[0];
    
    if (!regStudentId || !regStudentName || !imageFile) {
        resultDiv.className = 'result error';
        resultDiv.textContent = 'Please select an image' + (userRole === 'admin' ? ' and fill all fields' : '');
        return;
    }
    
    resultDiv.className = 'result';
    resultDiv.textContent = 'Registering student...';
    resultDiv.style.display = 'block';
    
    try {
        const imageBase64 = await getBase64(imageFile);
        
        const response = await fetch(`${API_BASE_URL}/register-face`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                studentId: regStudentId,
                name: regStudentName,
                image: imageBase64
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.className = 'result success';
            if (userRole === 'student') {
                resultDiv.textContent = data.message || 'Your face has been registered successfully!';
            } else {
                resultDiv.textContent = data.message || 'Student registered successfully!';
            }
            // Clear form (only image for students, all fields for admin)
            imageFileInput.value = '';
            const preview = document.getElementById('registerPreview');
            if (preview) preview.style.display = 'none';
            if (userRole === 'admin') {
                if (studentIdInput) studentIdInput.value = '';
                if (studentNameInput) studentNameInput.value = '';
            }
        } else {
            resultDiv.className = 'result error';
            resultDiv.textContent = data.error || 'Registration failed';
        }
    } catch (error) {
        resultDiv.className = 'result error';
        resultDiv.textContent = `Error: ${error.message}`;
    }
}

// Process attendance
async function processAttendance() {
    const classIdInput = document.getElementById('classId');
    const dateInput = document.getElementById('attendanceDate');
    const imageFileInput = document.getElementById('attendanceImage');
    const resultDiv = document.getElementById('attendanceResult');
    const studentsDiv = document.getElementById('identifiedStudents');
    
    if (!dateInput || !imageFileInput || !resultDiv) return;
    
    // For students, use default class ID or their student ID
    let classId = 'STUDENT';
    if (userRole === 'admin' && classIdInput) {
        classId = classIdInput.value.trim() || 'CS101';
    } else if (userRole === 'student') {
        classId = studentId || 'STUDENT'; // Use student ID as class ID for self-attendance
    }
    
    const date = dateInput.value;
    const imageFile = imageFileInput.files[0];
    
    if (!date || !imageFile) {
        resultDiv.className = 'result error';
        resultDiv.textContent = 'Please select a date and upload your photo';
        return;
    }
    
    resultDiv.className = 'result';
    resultDiv.textContent = 'Processing attendance...';
    resultDiv.style.display = 'block';
    if (studentsDiv) studentsDiv.innerHTML = '';
    
    try {
        const imageBase64 = await getBase64(imageFile);
        
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: imageBase64,
                classId: classId,
                date: date
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.className = 'result success';
            if (userRole === 'student') {
                // Check if student was identified
                const wasIdentified = data.identifiedStudents && data.identifiedStudents.some(s => s.studentId === studentId);
                if (wasIdentified) {
                    resultDiv.textContent = '✅ Your attendance has been recorded successfully!';
                } else {
                    resultDiv.textContent = '⚠️ Your face was not recognized. Please make sure you have uploaded your face first.';
                }
            } else {
                resultDiv.textContent = data.message;
            }
            
            // Display identified students
            if (studentsDiv && data.identifiedStudents && data.identifiedStudents.length > 0) {
                if (userRole === 'student') {
                    studentsDiv.innerHTML = '<h3>You were identified:</h3>';
                } else {
                    studentsDiv.innerHTML = '<h3>Identified Students:</h3>';
                }
                data.identifiedStudents.forEach(student => {
                    const card = document.createElement('div');
                    card.className = 'student-card';
                    const isYou = (userRole === 'student' && student.studentId === studentId);
                    card.innerHTML = `
                        <h4>${student.name}${isYou ? ' (You)' : ''}</h4>
                        <p>ID: ${student.studentId} | Confidence: ${student.confidence.toFixed(2)}%</p>
                    `;
                    studentsDiv.appendChild(card);
                });
            } else if (userRole === 'student') {
                studentsDiv.innerHTML = '<div class="result error">Your face was not recognized. Please upload your face first in the "Upload My Face" tab.</div>';
            }
            
            // Clear form
            imageFileInput.value = '';
            const preview = document.getElementById('attendancePreview');
            if (preview) preview.style.display = 'none';
            
            // Refresh dashboard
            loadAttendance();
        } else {
            resultDiv.className = 'result error';
            resultDiv.textContent = data.error || 'Processing failed';
        }
    } catch (error) {
        resultDiv.className = 'result error';
        resultDiv.textContent = `Error: ${error.message}`;
    }
}

// Load attendance records
async function loadAttendance() {
    const dateInput = document.getElementById('filterDate');
    const studentIdFilterInput = document.getElementById('filterStudentId');
    const listDiv = document.getElementById('attendanceList');
    
    if (!listDiv) return;
    
    const date = dateInput ? dateInput.value : '';
    const filterStudentId = studentIdFilterInput ? studentIdFilterInput.value : '';
    
    listDiv.innerHTML = '<div class="loading">Loading attendance records...</div>';
    
    try {
        let url = `${API_BASE_URL}/attendance?`;
        if (date) url += `date=${date}&`;
        
        // If student, only show their records
        if (userRole === 'student' && studentId) {
            url += `studentId=${studentId}&`;
        } else if (filterStudentId) {
            // Admin can filter by student ID
            url += `studentId=${filterStudentId}&`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            // Filter records for students (client-side safety check)
            let records = data.records;
            if (userRole === 'student' && studentId) {
                records = records.filter(r => r.studentId === studentId);
            }
            
            if (records.length === 0) {
                listDiv.innerHTML = '<div class="loading">No attendance records found</div>';
                return;
            }
            
            listDiv.innerHTML = '';
            records.forEach(record => {
                const card = document.createElement('div');
                card.className = 'attendance-card';
                card.innerHTML = `
                    <div>
                        <h4>${record.studentName}</h4>
                        <div class="meta">
                            ID: ${record.studentId} | Class: ${record.classId} | Date: ${record.date}
                            <br>Time: ${new Date(record.timestamp).toLocaleString()}
                        </div>
                    </div>
                    <div>
                        <span class="badge present">${record.status}</span>
                        <p style="margin-top: 5px; font-size: 0.8em; color: #666;">Confidence: ${record.confidence}%</p>
                    </div>
                `;
                listDiv.appendChild(card);
            });
        } else {
            listDiv.innerHTML = `<div class="result error">Error: ${data.error}</div>`;
        }
    } catch (error) {
        listDiv.innerHTML = `<div class="result error">Error: ${error.message}</div>`;
    }
}
