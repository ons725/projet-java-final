import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

export default function Home() {
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/courses')
      .then(r => r.json())
      .then(data => { setCourses(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <div className="loading">⏳ Chargement des cours...</div>

  return (
    <>
      <div className="stats-row">
        <div className="stat-box">
          <div className="num">{courses.length}</div>
          <div className="lbl">Cours disponibles</div>
        </div>
        <div className="stat-box">
          <div className="num">🐳</div>
          <div className="lbl">Dockerisé & prêt</div>
        </div>
        <div className="stat-box">
          <div className="num">✅</div>
          <div className="lbl">API connectée</div>
        </div>
      </div>

      <div className="alert alert-info" style={{ marginBottom: 24 }}>
        🎉 Bienvenue ! Sélectionnez un cours pour commencer. Votre progression est sauvegardée automatiquement.
      </div>

      <h3 style={{ marginBottom: 16, fontSize: 17, fontWeight: 600 }}>Tous les cours</h3>

      {courses.length === 0 ? (
        <div className="alert alert-error">Impossible de charger les cours. Vérifiez que le backend est démarré.</div>
      ) : (
        <div className="course-grid">
          {courses.map(course => (
            <Link to={`/courses/${course.id}`} key={course.id}>
              <div className="course-card">
                <div className="course-thumb">{course.emoji}</div>
                <div className="course-body">
                  <div className="course-title">{course.title}</div>
                  <div className="course-meta">
                    <span>👤 {course.instructor}</span>
                    <span>⏱ {course.duration}</span>
                    <span className={`badge ${course.level === 'Débutant' ? 'badge-green' : 'badge-orange'}`}>
                      {course.level}
                    </span>
                  </div>
                  <p style={{ fontSize: 13, color: 'var(--text2)', lineHeight: 1.5 }}>
                    {course.description.substring(0, 100)}…
                  </p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </>
  )
}