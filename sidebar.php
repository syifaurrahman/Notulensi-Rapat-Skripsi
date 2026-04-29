    <aside class="sidebar">
        <div class="logo-area">
            <span class="logo-icon"><i class="fas fa-pen-to-square"></i></span>
            <span class="logo-text">Notulensia</span>
            <button class="sidebar-close-btn" onclick="toggleSidebarMaster()" title="Sembunyikan Sidebar"><i class="fas fa-times"></i></button>
        </div>

        <div class="nav-menu">
            <!-- Dashboard - semua level -->
            <a href="dashboard.php" class="nav-item <?php echo isActive('dashboard.php'); ?>">
                <i class="fas fa-th-large"></i>
                <span>Dashboard</span>
            </a>

            <!-- Notulensi Dropdown - hanya Admin (level = 1) -->
            <?php if ($level_user == 1): ?>
                <?php
                    $notulensiActive = in_array(basename($_SERVER['PHP_SELF']), ['notulensi.php', 'notulensi_upload.php']);
                ?>
                <div class="nav-dropdown <?php echo $notulensiActive ? 'open' : ''; ?>">
                    <div class="nav-item nav-dropdown-toggle <?php echo $notulensiActive ? 'active' : ''; ?>" onclick="toggleDropdown(this)">
                        <i class="fas fa-file-alt"></i>
                        <span>Notulensi</span>
                        <i class="fas fa-chevron-down dropdown-chevron"></i>
                    </div>
                    <div class="nav-dropdown-menu">
                        <a href="notulensi.php" class="nav-sub-item <?php echo isActive('notulensi.php'); ?>">
                            <i class="fas fa-broadcast-tower"></i>
                            <span>Live</span>
                        </a>
                        <a href="notulensi_upload.php" class="nav-sub-item <?php echo isActive('notulensi_upload.php'); ?>">
                            <i class="fas fa-cloud-arrow-up"></i>
                            <span>Upload</span>
                        </a>
                    </div>
                </div>
            <?php endif; ?>

            <!-- Report - semua level -->
            <a href="report.php" class="nav-item <?php echo isActive('report.php'); ?>">
                <i class="fas fa-chart-pie"></i>
                <span>Report</span>
            </a>

            <!-- Pengaturan - semua level -->
            <a href="pengaturan.php" class="nav-item <?php echo isActive('pengaturan.php'); ?>">
                <i class="fas fa-cog"></i>
                <span>Pengaturan</span>
            </a>
        </div>

        <div class="sidebar-footer">
            <div class="user-info">
                <div class="user-avatar"><?php echo $inisial; ?></div>
                <div class="user-details">
                    <span class="user-name"><?php echo $nama_user; ?></span>
                    <span class="user-role"><?php echo ($level_user == 1) ? 'Admin' : 'User'; ?></span>
                </div>
            </div>
            <a href="proses/proses_logout.php" class="logout-btn">
                <i class="fas fa-sign-out-alt"></i> Logout
            </a>
        </div>
    </aside>
    <script src="assets/js/realtime-clock.js"></script>
    <script>
        function toggleDropdown(el) {
            const dropdown = el.closest('.nav-dropdown');
            const toggle = dropdown.querySelector('.nav-dropdown-toggle');
            const allNavItems = document.querySelectorAll('.nav-menu > a.nav-item');

            dropdown.classList.toggle('open');

            if (dropdown.classList.contains('open')) {
                allNavItems.forEach(item => item.classList.remove('active'));
                toggle.classList.add('active');
            } else {
                toggle.classList.remove('active');
                const currentPage = window.location.pathname.split('/').pop();
                allNavItems.forEach(item => {
                    const href = item.getAttribute('href');
                    if (href === currentPage) {
                        item.classList.add('active');
                    }
                });
            }
        }

        // --- Sidebar Toggle Logic ---
        function toggleSidebarMaster() {
            document.body.classList.toggle('sidebar-hidden');
            const isHidden = document.body.classList.contains('sidebar-hidden');
            localStorage.setItem('notulensi_sidebar_hidden', isHidden);
        }

        // Initialize and inject hamburger
        document.addEventListener("DOMContentLoaded", () => {
            // Restore state from localStorage
            if (localStorage.getItem('notulensi_sidebar_hidden') === 'true') {
                document.body.classList.add('sidebar-hidden');
            }

            // Inject Hamburger to top-bar
            const topBar = document.querySelector(".top-bar");
            const pageTitle = document.querySelector(".page-title");
            if (topBar && pageTitle) {
                const toggleBtn = document.createElement("button");
                toggleBtn.className = "header-toggle-btn";
                toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
                toggleBtn.title = "Tampilkan Sidebar";
                toggleBtn.onclick = toggleSidebarMaster;
                
                const wrapper = document.createElement("div");
                wrapper.className = "top-bar-left-wrapper";
                
                topBar.insertBefore(wrapper, pageTitle);
                wrapper.appendChild(toggleBtn);
                wrapper.appendChild(pageTitle);
            }
        });
    </script>