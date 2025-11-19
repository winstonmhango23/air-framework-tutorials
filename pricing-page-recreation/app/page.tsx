'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Check, X, Database, Zap, BarChart3, FileText, Shield, Sparkles, ArrowRight, Code, Layout, TrendingUp, Users, Lock, Clock, Globe, ChevronRight } from 'lucide-react'

export default function LandingPage() {
  const [isYearly, setIsYearly] = useState(true)

  const plans = [
    {
      name: 'Start here',
      price: 0,
      period: 'per month',
      features: [
        { text: 'Access to all modules', included: true },
        { text: 'Build first screen free', included: true },
        { text: 'Full Airtable integration', included: false },
        { text: '1:1 build sessions', included: false },
        { text: 'Sell memberships', included: false },
        { text: 'Premium support', included: false },
        { text: 'Connect to Shopify & WooCommerce', included: false },
        { text: 'Custom admin panel to manage users, data, etc', included: false },
      ],
      buttonText: 'Request Access',
      buttonVariant: 'outline' as const,
      subtext: "It's free so why not",
      highlighted: false,
    },
    {
      name: 'Startup',
      price: 8,
      period: 'per month',
      features: [
        { text: 'Access to all modules', included: true },
        { text: 'Build multiple screens', included: true },
        { text: 'Full Airtable integration', included: true },
        { text: '1:1 build sessions', included: true },
        { text: 'Sell memberships', included: true },
        { text: 'Premium support', included: false },
        { text: 'Connect to Shopify & WooCommerce', included: false },
        { text: 'Custom admin panel to manage users, data, etc', included: false },
      ],
      buttonText: 'Request Access',
      buttonVariant: 'default' as const,
      subtext: 'Save $72 per year',
      highlighted: true,
    },
    {
      name: 'Growth',
      price: 79,
      period: 'per month',
      features: [
        { text: 'Access to all modules', included: true },
        { text: 'Build multiple screens', included: true },
        { text: 'Full Airtable integration', included: true },
        { text: '1:1 build sessions', included: true },
        { text: 'Sell memberships', included: true },
        { text: 'Premium support', included: true },
        { text: 'Connect to Shopify & WooCommerce', included: true },
        { text: 'Custom admin panel to manage users, data, etc', included: true },
      ],
      buttonText: 'Request Access',
      buttonVariant: 'outline' as const,
      subtext: 'Save $440 per year',
      highlighted: false,
    },
  ]

  const faqs = [
    {
      question: 'What kind of apps can I build?',
      answer:
        'This is completely up to you. We have had apps ranging from "instagram for food," to marketplaces, to membership subscription apps, to a plethora of dating apps. It really is up to your creativity as a maker, truly. We have built this so that if you can design it, it can be published, made functional and with a database. Not creative but still want an app? No worries, we have 1:1 build sessions to show you how it\'s done. Check out some of our example apps here.',
    },
    {
      question: 'What happens to my app if I cancel?',
      answer:
        'We have built our platform with the non technical maker\'s (no coder) journey in mind. When you have a tech team of your own or just want to push the publish button, you can walk away with your source code at any time. Just go to publish and then hit the export source code button.',
    },
    {
      question: 'I see there\'s a fee to publish to the app stores and to export code? Why?',
      answer:
        'Simply put, it costs bandwidth to run builds through the app store and to publish source code. In addition, this can be looked at as a built-in quality control. We want makers to think about when they publish or export and not press publish a million times (this has happened when we didn\'t charge). So, in a manner of speaking the $99 fee is our first line of defense from publishing damage and running existing relationships (again, this has happened).',
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      {/* Navigation */}
      <nav className="border-b border-slate-800/50 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="flex size-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-violet-600">
                <BarChart3 className="size-6 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Auto-Stats</span>
            </div>
            <div className="hidden items-center gap-8 md:flex">
              <a href="#features" className="text-sm text-slate-300 hover:text-white transition-colors">Features</a>
              <a href="#how-it-works" className="text-sm text-slate-300 hover:text-white transition-colors">How It Works</a>
              <a href="#pricing" className="text-sm text-slate-300 hover:text-white transition-colors">Pricing</a>
              <Button className="bg-blue-600 hover:bg-blue-700 text-white">Get Started</Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-blue-500/10 via-transparent to-transparent" />
        <div className="absolute inset-0" style={{
          backgroundImage: 'radial-gradient(circle at 1px 1px, rgb(148 163 184 / 0.05) 1px, transparent 0)',
          backgroundSize: '40px 40px'
        }} />
        
        <div className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8 lg:py-32">
          <div className="text-center">
            <div className="inline-flex items-center gap-2 rounded-full bg-blue-500/10 px-4 py-2 text-sm text-blue-400 border border-blue-500/20 mb-6">
              <Sparkles className="size-4" />
              <span>AI-Powered Report Generation</span>
            </div>
            
            <h1 className="text-5xl font-bold tracking-tight text-white sm:text-6xl lg:text-7xl text-balance">
              Instant Reports from
              <span className="block bg-gradient-to-r from-blue-400 via-violet-400 to-purple-400 bg-clip-text text-transparent">
                Any Database
              </span>
            </h1>
            
            <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-300 leading-relaxed text-pretty">
              Auto-Stats automatically discovers your database schema, maps your API endpoints, and generates comprehensive HR and accounting reports with zero configuration. Connect once, report forever.
            </p>
            
            <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-6 text-lg rounded-xl">
                Start Free Trial
                <ArrowRight className="ml-2 size-5" />
              </Button>
              <Button size="lg" variant="outline" className="border-slate-700 text-white hover:bg-slate-800 px-8 py-6 text-lg rounded-xl">
                Watch Demo
              </Button>
            </div>
            
            <div className="mt-12 flex items-center justify-center gap-8 text-sm text-slate-400">
              <div className="flex items-center gap-2">
                <Check className="size-4 text-green-500" />
                <span>No code required</span>
              </div>
              <div className="flex items-center gap-2">
                <Check className="size-4 text-green-500" />
                <span>5-minute setup</span>
              </div>
              <div className="flex items-center gap-2">
                <Check className="size-4 text-green-500" />
                <span>Enterprise security</span>
              </div>
            </div>
          </div>

          {/* Dashboard Preview */}
          <div className="mt-20 rounded-2xl border border-slate-800/50 bg-slate-900/50 p-2 backdrop-blur-sm shadow-2xl">
            <div className="overflow-hidden rounded-xl bg-slate-950 border border-slate-800">
              <div className="flex items-center gap-2 border-b border-slate-800 px-4 py-3">
                <div className="size-3 rounded-full bg-red-500" />
                <div className="size-3 rounded-full bg-yellow-500" />
                <div className="size-3 rounded-full bg-green-500" />
              </div>
              <div className="p-8">
                <img 
                  src="/modern-analytics-dashboard-with-charts-tables-dark.jpg" 
                  alt="Dashboard Preview" 
                  className="w-full rounded-lg"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="relative py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white sm:text-4xl">
              Everything you need for automated reporting
            </h2>
            <p className="mt-4 text-lg text-slate-400">
              Powered by advanced AI that understands your data structure
            </p>
          </div>

          <div className="mt-16 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {[
              {
                icon: Database,
                title: 'Auto-Discovery',
                description: 'Automatically enumerates database tables, collections, and documents from any database system.',
                color: 'from-blue-500 to-cyan-500'
              },
              {
                icon: Code,
                title: 'API Mapping',
                description: 'Intelligently maps your API endpoints and data flows without manual configuration.',
                color: 'from-violet-500 to-purple-500'
              },
              {
                icon: BarChart3,
                title: 'Smart Dashboards',
                description: 'Generate beautiful, interactive dashboards with charts, tables, and KPIs automatically.',
                color: 'from-emerald-500 to-green-500'
              },
              {
                icon: FileText,
                title: 'Custom Reports',
                description: 'Create HR, accounting, and analytics reports with AI-powered insights and recommendations.',
                color: 'from-orange-500 to-red-500'
              },
              {
                icon: Zap,
                title: 'Real-Time Updates',
                description: 'Reports update automatically as your data changes, keeping insights always current.',
                color: 'from-pink-500 to-rose-500'
              },
              {
                icon: Shield,
                title: 'Enterprise Security',
                description: 'Bank-level encryption, SOC 2 compliance, and role-based access control included.',
                color: 'from-amber-500 to-yellow-500'
              }
            ].map((feature, idx) => (
              <div key={idx} className="group relative overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/50 p-8 hover:border-slate-700 transition-all hover:shadow-xl hover:shadow-blue-500/10">
                <div className={`inline-flex rounded-xl bg-gradient-to-br ${feature.color} p-3`}>
                  <feature.icon className="size-6 text-white" />
                </div>
                <h3 className="mt-6 text-xl font-semibold text-white">{feature.title}</h3>
                <p className="mt-3 text-slate-400 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="relative py-24 bg-slate-900/30">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white sm:text-4xl">
              From connection to insights in minutes
            </h2>
            <p className="mt-4 text-lg text-slate-400">
              Three simple steps to automated reporting
            </p>
          </div>

          <div className="mt-16 grid gap-12 lg:grid-cols-3">
            {[
              {
                step: '01',
                title: 'Connect Your Database',
                description: 'Simply provide your database credentials. We support PostgreSQL, MySQL, MongoDB, and 20+ other databases.',
                icon: Database
              },
              {
                step: '02',
                title: 'AI Auto-Configuration',
                description: 'Our AI analyzes your schema, discovers relationships, and maps out your entire data structure automatically.',
                icon: Sparkles
              },
              {
                step: '03',
                title: 'Generate Reports',
                description: 'Start creating dashboards, exporting reports, and gaining insights immediately. No setup required.',
                icon: TrendingUp
              }
            ].map((step, idx) => (
              <div key={idx} className="relative">
                {idx < 2 && (
                  <div className="absolute top-16 left-full hidden h-0.5 w-full bg-gradient-to-r from-blue-500/50 to-transparent lg:block" />
                )}
                <div className="relative rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
                  <div className="text-6xl font-bold text-slate-800">{step.step}</div>
                  <div className="mt-4 inline-flex rounded-xl bg-blue-500/10 p-3 border border-blue-500/20">
                    <step.icon className="size-6 text-blue-400" />
                  </div>
                  <h3 className="mt-6 text-xl font-semibold text-white">{step.title}</h3>
                  <p className="mt-3 text-slate-400 leading-relaxed">{step.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="relative py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="rounded-3xl border border-slate-800 bg-gradient-to-br from-blue-900/20 to-violet-900/20 p-12 backdrop-blur-sm">
            <div className="grid gap-8 md:grid-cols-4">
              {[
                { value: '10K+', label: 'Active Users', icon: Users },
                { value: '99.9%', label: 'Uptime SLA', icon: TrendingUp },
                { value: '<2min', label: 'Avg Setup Time', icon: Clock },
                { value: '50+', label: 'Integrations', icon: Globe }
              ].map((stat, idx) => (
                <div key={idx} className="text-center">
                  <stat.icon className="mx-auto size-8 text-blue-400 mb-4" />
                  <div className="text-4xl font-bold text-white">{stat.value}</div>
                  <div className="mt-2 text-sm text-slate-400">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Database Integrations */}
      <section className="relative py-24 bg-slate-900/30">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white sm:text-4xl">
              Works with your existing infrastructure
            </h2>
            <p className="mt-4 text-lg text-slate-400">
              Connect to any database or data source
            </p>
          </div>

          <div className="mt-16 grid grid-cols-2 gap-8 md:grid-cols-4 lg:grid-cols-6">
            {['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'SQLite', 'MariaDB', 
              'Oracle', 'SQL Server', 'Firebase', 'Supabase', 'DynamoDB', 'Cassandra'].map((db, idx) => (
              <div key={idx} className="flex items-center justify-center rounded-xl border border-slate-800 bg-slate-900/50 p-6 hover:border-slate-700 transition-colors">
                <span className="text-sm font-medium text-slate-400">{db}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="relative py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center">
            <h2 className="text-5xl font-bold tracking-tight text-white">Pricing</h2>
            <p className="mt-4 text-slate-400">
              You can stay on the $6 plan until you have enough active users
              <br />
              to justify managing their data or you start selling things.
            </p>

            {/* Toggle */}
            <div className="mt-8 inline-flex items-center gap-2 rounded-full bg-slate-800/50 p-1 border border-slate-700">
              <button
                onClick={() => setIsYearly(true)}
                className={`rounded-full px-6 py-2 text-sm font-medium transition-all ${
                  isYearly
                    ? 'bg-emerald-500 text-black'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Billed yearly <span className="ml-1">-43%</span>
              </button>
              <button
                onClick={() => setIsYearly(false)}
                className={`rounded-full px-6 py-2 text-sm font-medium transition-all ${
                  !isYearly
                    ? 'bg-emerald-500 text-black'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Billed monthly
              </button>
            </div>
          </div>

          {/* Pricing Cards */}
          <div className="mt-16 grid gap-8 lg:grid-cols-3">
            {plans.map((plan) => (
              <div
                key={plan.name}
                className={`relative rounded-3xl bg-slate-900/50 p-8 backdrop-blur-sm ${
                  plan.highlighted
                    ? 'border-2 border-emerald-500 shadow-lg shadow-emerald-500/20'
                    : 'border border-slate-800'
                }`}
              >
                {/* Plan Header */}
                <div className="text-center">
                  <h3
                    className={`text-lg font-medium ${
                      plan.highlighted ? 'text-emerald-500' : 'text-blue-400'
                    }`}
                  >
                    {plan.name}
                  </h3>
                  <div className="mt-4">
                    <span className="text-5xl font-bold text-white">${plan.price}</span>
                  </div>
                  <p className="mt-2 text-sm text-slate-400">{plan.period}</p>
                </div>

                {/* Features */}
                <ul className="mt-8 space-y-4">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-start gap-3">
                      {feature.included ? (
                        <Check className="mt-0.5 size-5 shrink-0 text-emerald-500" />
                      ) : (
                        <X className="mt-0.5 size-5 shrink-0 text-slate-700" />
                      )}
                      <span
                        className={`text-sm ${
                          feature.included ? 'text-white' : 'text-slate-600'
                        }`}
                      >
                        {feature.text}
                      </span>
                    </li>
                  ))}
                </ul>

                {/* CTA Button */}
                <div className="mt-8">
                  <Button
                    className={`w-full rounded-full py-6 font-medium ${
                      plan.highlighted
                        ? 'bg-emerald-500 text-black hover:bg-emerald-400'
                        : 'border-2 border-slate-700 bg-transparent text-white hover:border-slate-600 hover:bg-slate-800'
                    }`}
                    variant={plan.buttonVariant}
                  >
                    {plan.buttonText}
                  </Button>
                  <p className="mt-3 text-center text-xs text-slate-500">
                    {plan.subtext}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* Footer Note */}
          <p className="mt-12 text-center text-sm text-slate-500">
            There is a one-time $99 fee to publish your app and/or export source
            code
          </p>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="relative py-24 bg-slate-900/30">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center text-4xl font-bold text-white">
            Frequently Asked Questions
          </h2>

          <div className="mt-12 space-y-8">
            {faqs.map((faq, index) => (
              <div key={index} className="rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
                <h3 className="text-xl font-semibold text-white">{faq.question}</h3>
                <p className="mt-4 text-slate-400 leading-relaxed">
                  {faq.answer}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-br from-blue-900/40 via-violet-900/40 to-purple-900/40 p-12 text-center backdrop-blur-sm lg:p-20">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(120,119,198,0.3),rgba(255,255,255,0))]" />
            <div className="relative">
              <h2 className="text-4xl font-bold text-white sm:text-5xl text-balance">
                Ready to automate your reporting?
              </h2>
              <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-300">
                Join thousands of companies using Auto-Stats to transform their data into actionable insights
              </p>
              <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
                <Button size="lg" className="bg-white text-slate-900 hover:bg-slate-100 px-8 py-6 text-lg rounded-xl">
                  Start Free Trial
                  <ChevronRight className="ml-2 size-5" />
                </Button>
                <Button size="lg" variant="outline" className="border-white/20 text-white hover:bg-white/10 px-8 py-6 text-lg rounded-xl">
                  Schedule Demo
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative border-t border-slate-800 py-12">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-8 md:grid-cols-4">
            <div>
              <div className="flex items-center gap-2">
                <div className="flex size-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-violet-600">
                  <BarChart3 className="size-6 text-white" />
                </div>
                <span className="text-xl font-bold text-white">Auto-Stats</span>
              </div>
              <p className="mt-4 text-sm text-slate-400">
                AI-powered reporting for modern teams
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-white">Product</h4>
              <ul className="mt-4 space-y-2 text-sm text-slate-400">
                <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Integrations</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Changelog</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white">Company</h4>
              <ul className="mt-4 space-y-2 text-sm text-slate-400">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white">Legal</h4>
              <ul className="mt-4 space-y-2 text-sm text-slate-400">
                <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-12 border-t border-slate-800 pt-8 text-center text-sm text-slate-400">
            <p>&copy; 2025 Auto-Stats. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
