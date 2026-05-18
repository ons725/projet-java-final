import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

function renderContent(text) {
  // Simple renderer for code blocks and bold
  const parts = text.split(/(```[\s\S]*?```|\*\*[^*]+\*\*)/g)
  return parts.map((part, i) => {
    if (part.startsWith('```') && part.endsWith('```')) {
      const code = part.slice(3, -3).replace(/^[a-z]*\n/, '')
      return <pre key={i}><code>{code}</code></pre>
    }
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>
    }
    return <span key={i}>{part}</span>
  })
}

export default function Course() {
  const { id } = useParams()
  const [course, setCourse] = useState(null)
  const [lessons, setLessons] = useState([])
  const [current, setCurrent] = useState(0)
  const [completed, setCompleted] = useState([])
  const [saving, setSaving] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch(`/api/courses/${id}`).then(r => r.json()),
      fetch(`/api/courses/${id}/lessons`).then(r => r.json()),
      fetch(`/api/progress/${id}`).then(r => r.json()),
    ]).then(([c, l, p]) => {
      setCourse(c)
      setLessons(l)
      setCompleted(p.completed_lessons || [])
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [id])

  const markDone = async () => {
    if (!lessons[current]) return
    const lesson = lessons[current]
    setSaving(true)
    await fetch('/api/progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ course_id: parseInt(id), lesson_id: lesson.id, done: true })
    })
    setCompleted(prev => [...new Set([...prev, lesson.id])])
    setSaving(false)
    if (current < lessons.length - 1) setCurrent(current + 1)
  }

  if (loading) return <div className="loading">⏳ Chargement...</div>
  if (!course) return <div className="alert alert-error">Cours introuvable.</div>

  const lesson = lessons[current]
  const pct = lessons.length ? Math.round((completed.length / lessons.length) * 100) : 0

  return (
    <>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20, flexWrap: 'wrap' }}>
        <Link to="/" className="btn btn-outline btn-sm">← Retour</Link>
        <span style={{ fontSize: 22 }}>{course.emoji}</span>
        <div>
          <h2 style={{ fontSize: 18, fontWeight: 700 }}>{course.title}</h2>
          <div style={{ fontSize: 13, color: 'var(--text2)' }}>
            {course.instructor} · {course.duration} · {course.level}
          </div>
        </div>
        <div style={{ marginLeft: 'auto', textAlign: 'right' }}>
          <div style={{ fontSize: 13, color: 'var(--text2)', marginBottom: 4 }}>Progression : <strong>{pct}%</strong></div>
          <div className="progress-wrap" style={{ width: 140 }}>
            <div className="progress-fill" style={{ width: `${pct}%` }} />
          </div>
        </div>
      </div>

      <div className="lesson-layout">
        {/* Lesson list */}
        <div className="lesson-list">
          <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--border)', fontWeight: 600, fontSize: 13, color: 'var(--text2)', textTransform: 'uppercase', letterSpacing: 1 }}>
            Leçons ({lessons.length})
          </div>
          {lessons.map((l, i) => (
            <div
              key={l.id}
              className={`lesson-item ${i === current ? 'active' : ''} ${completed.includes(l.id) ? 'done' : ''}`}
              onClick={() => setCurrent(i)}
            >
              <div className="lesson-num">
                {completed.includes(l.id) ? '✓' : i + 1}
              </div>
              <span style={{ fontSize: 13 }}>{l.title}</span>
            </div>
          ))}
          <div style={{ padding: 12 }}>
            <Link to={`/courses/${id}/quiz`} className="btn btn-outline btn-sm" style={{ width: '100%', justifyContent: 'center' }}>
              🧠 Passer le quiz
            </Link>
          </div>
        </div>

        {/* Lesson content */}
        <div className="lesson-content">
          {lesson ? (
            <>
              <h2>{lesson.title}</h2>
              {completed.includes(lesson.id) && (
                <div className="alert alert-success">✅ Leçon complétée !</div>
              )}
              <div className="lesson-text" style={{ marginBottom: 24 }}>
                {lesson.content.split('\n').map((line, i) => {
                  if (!line.trim()) return <br key={i} />
                  return <p key={i}>{renderContent(line)}</p>
                })}
              </div>
              <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                {!completed.includes(lesson.id) && (
                  <button className="btn btn-success" onClick={markDone} disabled={saving}>
                    {saving ? '⏳ Sauvegarde...' : '✓ Marquer comme terminé'}
                  </button>
                )}
                {current > 0 && (
                  <button className="btn btn-outline" onClick={() => setCurrent(current - 1)}>← Précédent</button>
                )}
                {current < lessons.length - 1 && (
                  <button className="btn btn-primary" onClick={() => setCurrent(current + 1)}>Suivant →</button>
                )}
              </div>
            </>
          ) : (
            <div className="loading">Aucune leçon disponible.</div>
          )}
        </div>
      </div>
    </>
  )
}