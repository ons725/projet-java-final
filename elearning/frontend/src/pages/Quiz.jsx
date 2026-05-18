import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

const LETTERS = ['a', 'b', 'c', 'd']
const LABELS = ['A', 'B', 'C', 'D']

export default function Quiz() {
  const { id } = useParams()
  const [questions, setQuestions] = useState([])
  const [current, setCurrent] = useState(0)
  const [selected, setSelected] = useState(null)
  const [result, setResult] = useState(null)
  const [score, setScore] = useState(0)
  const [done, setDone] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`/api/courses/${id}/quiz`)
      .then(r => r.json())
      .then(data => { setQuestions(data); setLoading(false) })
  }, [id])

  const check = async () => {
    if (!selected) return
    const q = questions[current]
    const res = await fetch('/api/quiz/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quiz_id: q.id, answer: selected })
    })
    const data = await res.json()
    setResult(data)
    if (data.correct) setScore(s => s + 1)
  }

  const next = () => {
    if (current + 1 >= questions.length) {
      setDone(true)
    } else {
      setCurrent(current + 1)
      setSelected(null)
      setResult(null)
    }
  }

  if (loading) return <div className="loading">⏳ Chargement du quiz...</div>

  if (done) {
    const pct = Math.round((score / questions.length) * 100)
    return (
      <div style={{ maxWidth: 560, margin: '0 auto', textAlign: 'center', padding: '40px 20px' }}>
        <div style={{ fontSize: 64, marginBottom: 16 }}>{pct >= 70 ? '🏆' : '📚'}</div>
        <h2 style={{ fontSize: 24, marginBottom: 8 }}>Quiz terminé !</h2>
        <p style={{ color: 'var(--text2)', marginBottom: 24 }}>Votre score final</p>
        <div style={{ fontSize: 52, fontWeight: 800, color: pct >= 70 ? 'var(--success)' : 'var(--accent)', marginBottom: 8 }}>
          {pct}%
        </div>
        <p style={{ color: 'var(--text2)', marginBottom: 32 }}>{score} / {questions.length} réponses correctes</p>
        {pct >= 70 ? (
          <div className="alert alert-success">🎉 Félicitations ! Vous avez réussi ce quiz.</div>
        ) : (
          <div className="alert alert-error">Continuez à réviser et réessayez !</div>
        )}
        <div style={{ display: 'flex', gap: 10, justifyContent: 'center', marginTop: 16 }}>
          <Link to={`/courses/${id}`} className="btn btn-outline">← Retour au cours</Link>
          <button className="btn btn-primary" onClick={() => { setCurrent(0); setSelected(null); setResult(null); setScore(0); setDone(false) }}>
            🔄 Recommencer
          </button>
        </div>
      </div>
    )
  }

  if (questions.length === 0) return (
    <div style={{ textAlign: 'center', padding: 40 }}>
      <p style={{ color: 'var(--text2)', marginBottom: 16 }}>Pas de questions pour ce cours.</p>
      <Link to={`/courses/${id}`} className="btn btn-outline">← Retour</Link>
    </div>
  )

  const q = questions[current]
  const options = [q.option_a, q.option_b, q.option_c, q.option_d]

  return (
    <div style={{ maxWidth: 620, margin: '0 auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20 }}>
        <Link to={`/courses/${id}`} className="btn btn-outline btn-sm">← Retour</Link>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 13, color: 'var(--text2)', marginBottom: 6 }}>
            Question {current + 1} / {questions.length}
          </div>
          <div className="progress-wrap">
            <div className="progress-fill" style={{ width: `${((current) / questions.length) * 100}%` }} />
          </div>
        </div>
        <div style={{ fontWeight: 700, color: 'var(--success)' }}>Score : {score}</div>
      </div>

      <div className="card" style={{ marginBottom: 16 }}>
        <div className="card-body">
          <p style={{ fontSize: 16, fontWeight: 600, marginBottom: 20, lineHeight: 1.5 }}>
            {q.question}
          </p>

          {options.map((opt, i) => {
            let cls = 'quiz-option'
            if (result) {
              if (LETTERS[i] === result.correct_answer) cls += ' correct'
              else if (LETTERS[i] === selected) cls += ' wrong'
            } else if (selected === LETTERS[i]) cls += ' selected'
            return (
              <div
                key={i}
                className={cls}
                onClick={() => !result && setSelected(LETTERS[i])}
                style={{ cursor: result ? 'default' : 'pointer' }}
              >
                <div className="option-letter">{LABELS[i]}</div>
                <span>{opt}</span>
                {result && LETTERS[i] === result.correct_answer && (
                  <span style={{ marginLeft: 'auto', color: 'var(--success)', fontWeight: 700 }}>✓</span>
                )}
                {result && LETTERS[i] === selected && !result.correct && (
                  <span style={{ marginLeft: 'auto', color: 'var(--danger)', fontWeight: 700 }}>✗</span>
                )}
              </div>
            )
          })}

          {result && (
            <div className={`alert ${result.correct ? 'alert-success' : 'alert-error'}`} style={{ marginTop: 14 }}>
              {result.correct
                ? '✅ Bonne réponse ! Continuez ainsi.'
                : `❌ Incorrect. La bonne réponse est ${result.correct_answer.toUpperCase()}.`}
            </div>
          )}
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10 }}>
        {!result ? (
          <button className="btn btn-primary" onClick={check} disabled={!selected}>
            Valider →
          </button>
        ) : (
          <button className="btn btn-primary" onClick={next}>
            {current + 1 >= questions.length ? '🏁 Voir résultats' : 'Question suivante →'}
          </button>
        )}
      </div>
    </div>
  )
}