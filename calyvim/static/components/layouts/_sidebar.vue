<script setup>
const props = defineProps(['activePage'])
</script>

<template>
  <div
    class="sidebar border border-right col-md-3 col-lg-2 p-0 bg-body-tertiary"
  >
    <div
      class="offcanvas-md offcanvas-end bg-body-tertiary"
      tabindex="-1"
      id="sidebarMenu"
      aria-labelledby="sidebarMenuLabel"
    >
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="sidebarMenuLabel">Calyvim</h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="offcanvas"
          data-bs-target="#sidebarMenu"
          aria-label="Close"
        ></button>
      </div>
      <div
        class="offcanvas-body d-md-flex flex-column p-0 pt-lg-3 overflow-y-auto"
      >
        <ul class="nav flex-column">
          <li class="nav-item">
            <a
              class="nav-link d-flex align-items-center gap-2"
              :class="{ active: props.activePage === 'overview' }"
              href="/overview"
            >
              <svg class="bi">
                <use xlink:href="#house-fill" />
              </svg>
              Overview
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link d-flex align-items-center gap-2" href="#">
              <svg class="bi">
                <use xlink:href="#file-earmark" />
              </svg>
              Events
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link d-flex align-items-center gap-2" href="#">
              <svg class="bi">
                <use xlink:href="#cart" />
              </svg>
              Schedules
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link d-flex align-items-center gap-2" href="#">
              <svg class="bi">
                <use xlink:href="#people" />
              </svg>
              Bookings
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link d-flex align-items-center gap-2" href="#">
              <svg class="bi">
                <use xlink:href="#graph-up" />
              </svg>
              Account
            </a>
          </li>
          <li class="nav-item">
            <a
              class="nav-link d-flex align-items-center gap-2"
              href="/accounts/connected-accounts"
              :class="{ active: props.activePage === 'integrations' }"
            >
              <svg class="bi">
                <use xlink:href="#puzzle" />
              </svg>
              Integrations
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
/*
 * Sidebar
 */

@media (min-width: 768px) {
  .sidebar .offcanvas-lg {
    position: -webkit-sticky;
    position: sticky;
    top: 48px;
  }
  .navbar-search {
    display: block;
  }
}

.sidebar {
  height: 100vh;
}

.sidebar .nav-link {
  font-size: 0.875rem;
  font-weight: 500;
  color: black;
}

.sidebar .nav-link.active {
  border-right: 4px solid #2470dc;
  background: #e9e8ec;
}

.sidebar-heading {
  font-size: 0.75rem;
}
</style>
