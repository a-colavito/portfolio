'use client'

import { useState } from 'react'

export default function ContattiPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  })
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setStatus('loading')

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error('Errore nell\'invio')
      }

      setStatus('success')
      setFormData({ name: '', email: '', message: '' })
      setTimeout(() => setStatus('idle'), 5000)
    } catch (error) {
      setStatus('error')
      setTimeout(() => setStatus('idle'), 5000)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  return (
    <section>
      <h1 className="font-semibold text-2xl mb-8 tracking-tighter">Contact</h1>
      
      <p className="mb-4">
        Hello! I'm a developer passionate about building great web experiences.
        You can learn more about my background in my{' '}
        <a href="#" className="underline">resume</a>.
      </p>

      <p className="mb-6">
        Have an idea to share, a collaboration proposal, or just want to chat?
        Fill out the form below and I'll be happy to hear from you!
      </p>

      <form onSubmit={handleSubmit} className="space-y-4 max-w-lg">
        <div>
          <label htmlFor="name" className="block text-sm font-medium mb-2">Name:</label>
          <input type="text" id="name" name="name" value={formData.name} onChange={handleChange} required className="w-full px-4 py-2 border border-neutral-200 dark:border-neutral-800 rounded-lg bg-white dark:bg-black focus:outline-none focus:ring-2 focus:ring-neutral-400 dark:focus:ring-neutral-600" />
        </div>

        <div>
          <label htmlFor="email" className="block text-sm font-medium mb-2">Email:</label>
          <input type="email" id="email" name="email" value={formData.email} onChange={handleChange} required className="w-full px-4 py-2 border border-neutral-200 dark:border-neutral-800 rounded-lg bg-white dark:bg-black focus:outline-none focus:ring-2 focus:ring-neutral-400 dark:focus:ring-neutral-600" />
        </div>

        <div>
          <label htmlFor="message" className="block text-sm font-medium mb-2">Message:</label>
          <textarea id="message" name="message" value={formData.message} onChange={handleChange} required rows={5} className="w-full px-4 py-2 border border-neutral-200 dark:border-neutral-800 rounded-lg bg-white dark:bg-black focus:outline-none focus:ring-2 focus:ring-neutral-400 dark:focus:ring-neutral-600 resize-none" />
        </div>

        <button type="submit" disabled={status === 'loading'} className="px-6 py-2 bg-black dark:bg-white text-white dark:text-black rounded-lg hover:bg-neutral-800 dark:hover:bg-neutral-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium">
          {status === 'loading' ? 'Sending...' : 'Send'}
        </button>

        {status === 'success' && (
          <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
            <p className="text-green-800 dark:text-green-200 text-sm">✓ Message sent successfully! I'll get back to you soon.</p>
          </div>
        )}

        {status === 'error' && (
          <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-red-800 dark:text-red-200 text-sm">✗ Error sending message. Please try again.</p>
          </div>
        )}
      </form>
    </section>
  )
}
