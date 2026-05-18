import { Routes, Route, NavLink, useLocation } from 'react-router-dom'
import Home from './pages/Home.jsx'
import Course from './pages/Course.jsx'
import Quiz from './pages/Quiz.jsx'

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <h1>🎓 EduPortal</h1>
        <p>Université Digitale</p>
      </div>
      <nav className="sidebar-nav">
        <NavLink to="/" end className={({ isActive }) => 'nav-link' + (isActive ? ' active' : '')}>
          <span className="nav-icon">🏠</span> Accueil
        </NavLink>
        <NavLink to="/courses" className={({ isActive }) => 'nav-link' + (isActive ? ' active' : '')}>
          <span className="nav-icon">📚</span> Cours
        </NavLink>
      </nav>
    </aside>
  )
}

function PageWrapper({ title, children }) {
  return (
    <>
      <header className="topbar">
        <h2>{title}</h2>
      </header>
      <main className="content">{children}</main>
    </>
  )
}

export default function App() {
  const location = useLocation()

  const getTitle = () => {
    if (location.pathname === '/') return 'Tableau de bord'
    if (location.pathname.startsWith('/courses') && location.pathname.includes('/quiz')) return 'Quiz'
    if (location.pathname.startsWith('/courses/')) return 'Cours'
    if (location.pathname === '/courses') return 'Tous les cours'
    return 'EduPortal'
  }

  return (
    <div className="layout">
      <Sidebar />
      <div className="main">
        <PageWrapper title={getTitle()}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/courses" element={<Home />} />
            <Route path="/courses/:id" element={<Course />} />
            <Route path="/courses/:id/quiz" element={<Quiz />} />
          </Routes>
        </PageWrapper>
      </div>
    </div>
  )
}