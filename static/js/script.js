// ==========================================================
// ملف: script.js (FINAL CLEAN VERSION)
// يحتوي على وظائف الـ Frontend الأساسية
// ==========================================================

// ---------------------------------------------
// 1. وظيفة القائمة الجانبية (Hamburger Menu Logic)
// ---------------------------------------------
// في ملف script.js (قم بتنفيذ هذا الكود داخل الـ DOMContentLoaded أو أينما تريد)

// 1. تحديد العناصر بالـ ID الصحيح
const menuToggleBtn = document.getElementById('menu-toggle');
const navList = document.getElementById('main-nav-links');

// 2. ربط زر الهامبرغر بوظيفة التبديل
if (menuToggleBtn && navList) {
    menuToggleBtn.addEventListener("click", () => {
        // A. تبديل الكلاس على قائمة الروابط
        navList.classList.toggle("open"); 
        
        // B. تغيير الأيقونة (Fa-bars <-> Fa-times)
        const icon = menuToggleBtn.querySelector('i');
        if (navList.classList.contains('open')) {
            icon.classList.replace('fa-bars', 'fa-times');
        } else {
            icon.classList.replace('fa-times', 'fa-bars');
        }
    });
}

// ---------------------------------------------
// 2. دالة الوضع الليلي/النهاري (Dark/Light Mode)
// ---------------------------------------------
function toggleTheme() {
    const body = document.body;
    const btnIcon = document.querySelector('#theme-toggle i');
    
    body.classList.toggle('light-mode');
    
    // تغيير الأيقونة وحفظ الحالة
    if (body.classList.contains('light-mode')) {
        btnIcon.classList.replace('fa-sun', 'fa-moon');
        localStorage.setItem('theme', 'light'); 
    } else {
        btnIcon.classList.replace('fa-moon', 'fa-sun');
        localStorage.setItem('theme', 'dark');
    }
}

// ---------------------------------------------
// 3. تأثير الكتابة التلقائية (Typewriter Effect)
// ---------------------------------------------
function initializeTypewriter() {
    const typingElements = document.querySelectorAll('.typing-effect'); // 🚨 تم تعديل الكلاس لـ .typing-effect (كما في HTML)

    typingElements.forEach((element) => {
        const text = element.getAttribute('data-text');
        if (text) {
            element.innerText = '';
            let index = 0;
            function typeWriter() {
                if (index < text.length) {
                    element.innerText += text.charAt(index);
                    index++;
                    setTimeout(typeWriter, 100);
                }
            }
            typeWriter();
        }
    });
}


// ---------------------------------------------
// 4. تهيئة الصفحة عند التحميل (Initialization)
// ---------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    // A. استرجاع الوضع الليلي/النهاري
    const savedTheme = localStorage.getItem('theme');
    const themeToggleBtn = document.getElementById('theme-toggle');

    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        if (themeToggleBtn) {
             themeToggleBtn.querySelector('i').classList.replace('fa-sun', 'fa-moon');
        }
    }
    
    // B. تفعيل تأثير Typewriter
    initializeTypewriter();
    
    // C. ربط زرار الهامبرغر مباشرة (للتأكد من عمله)
    const mobileToggle = document.getElementById('menu-toggle');
    if (mobileToggle) {
        // نستخدم addEventListener كإجراء أمان إضافي للـ onclick
        mobileToggle.addEventListener('click', toggleMobileMenu);
    }
});



// في ملف server.html (داخل وسم <script>)
function openTab(tabName, btn) {
    // ...
    // تأكد من إضافة id="working" للإخفاء والإظهار
    document.getElementById('iptv').style.display = 'none';
    document.getElementById('cccam').style.display = 'none';
    document.getElementById('working').style.display = 'none'; // 👈 إضافة
    
    document.getElementById(tabName).style.display = 'block';
    // ...
}



/* كود فتح وإغلاق القائمة الجانبية (Sidebar)
   بيشتغل لما تدوس على زرار الهامبرجر أو زرار الإغلاق أو الخلفية الشفافة
*/
function toggleMenu() {
    // 1. يمسك عنصر القائمة الجانبية
    const sidebar = document.getElementById('sidebarMenu');
    
    // 2. يمسك عنصر الخلفية المعتمة (Overlay)
    const overlay = document.getElementById('overlay');
    
    // 3. يبدل الكلاس 'active' (لو موجود يشيله، ولو مش موجود يحطه)
    if (sidebar && overlay) {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    } else {
        console.error("العناصر sidebarMenu أو overlay غير موجودة في الصفحة!");
    }
}

/* كود القائمة العائمة (لو لسه بتستخدمها في الدعم الفني مثلاً)
*/
function toggleFloatMenu() {
    const floatMenu = document.getElementById('floatMenu');
    if (floatMenu) {
        floatMenu.classList.toggle('active');
    }
}

function toggleMenu() {
    const sidebar = document.getElementById('sidebarMenu');
    const overlay = document.getElementById('overlay');
    
    // بيبدل الكلاس active (لو موجود يشيله ولو مش موجود يحطه)
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}