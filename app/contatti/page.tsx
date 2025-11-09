'use client'

import { useState } from 'react'

export default function ContattiPage() {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setStatus('loading')

    const form = e.currentTarget
    const formData = new FormData(form)

    try {
      const response = await fetch('https://formspree.io/f/mzzrwdkd', {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json'
        }
      })

      if (response.ok) {
        setStatus('success')
        form.reset()
        setTimeout(() => setStatus('idle'), 5000)
      } else {
        setStatus('error')
        setTimeout(() => setStatus('idle'), 5000)
      }
    } catch (error) {
      setStatus('error')
      setTimeout(() => setStatus('idle'), 5000)
    }
  }

  return (
    <section>
      <h1 className="font-semibold text-2xl mb-8 tracking-tighter">Contatti</h1>
      
      <p className="mb-4 leading-relaxed">
        Ciao! Sono Adolfo, classe '97, diplomato al classico e attualmente studente
        presso la facoltà di Ingegneria Informatica del Politecnico di Bari, ma queste cose
        potrai leggerle nel <a href="https://res.cloudinary.com/dkkvkj82k/image/upload/v1749566768/CV_it_dby0co.pdf" target="_blank" rel="noopener noreferrer" className="underline break-words">curriculum</a>, quindi saltiamo alla parte meno noiosa ecco una lista di cose che mi piacciono:
      </p>

      <ul className="list-disc list-inside mb-6 space-y-1">
        <li>I gatti</li>
        <li>Correre</li>
        <li>I Radiohead</li>
      </ul>

      <p className="mb-6 text-sm sm:text-base leading-relaxed">
        Hai un'idea da condividere, una proposta di collaborazione o semplicemente vuoi fare due chiacchiere? Compila il form qui sotto, e sarò felice di sentirti!
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium mb-2">Nome:</label>
          <input type="text" id="name" name="name" required className="w-full px-4 py-2 border border-neutral-200 dark:border-neutral-800 rounded-lg bg-white dark:bg-black focus:outline-none focus:ring-2 focus:ring-neutral-400 dark:focus:ring-neutral-600" />
        </div>

        <div>
          <label htmlFor="email" className="block text-sm font-medium mb-2">Email:</label>
          <input type="email" id="email" name="email" required className="w-full px-4 py-2 border border-neutral-200 dark:border-neutral-800 rounded-lg bg-white dark:bg-black focus:outline-none focus:ring-2 focus:ring-neutral-400 dark:focus:ring-neutral-600" />
        </div>

        <div>
          <label htmlFor="message" className="block text-sm font-medium mb-2">Messaggio:</label>
          <textarea id="message" name="message" required rows={5} className="w-full px-4 py-2 border border-neutral-200 dark:border-neutral-800 rounded-lg bg-white dark:bg-black focus:outline-none focus:ring-2 focus:ring-neutral-400 dark:focus:ring-neutral-600 resize-none" />
        </div>

        <button type="submit" disabled={status === 'loading'} className="px-6 py-2 bg-black dark:bg-white text-white dark:text-black rounded-lg hover:bg-neutral-800 dark:hover:bg-neutral-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium">
          {status === 'loading' ? 'Invio in corso...' : 'Invia'}
        </button>

        {status === 'success' && (
          <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
            <p className="text-green-800 dark:text-green-200">✓ Messaggio inviato con successo! Ti risponderò presto.</p>
          </div>
        )}

        {status === 'error' && (
          <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-red-800 dark:text-red-200">✗ Errore nell'invio del messaggio. Riprova.</p>
          </div>
        )}
      </form>

      <p className="text-sm text-neutral-600 dark:text-neutral-400 italic mt-6">(Prometto che leggo anche la cartella spam! 📧)</p>
    </section>
  )
}
