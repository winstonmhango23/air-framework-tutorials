// Pricing page functionality
document.addEventListener('DOMContentLoaded', function() {
    const yearlyToggle = document.getElementById('yearly-toggle');
    const monthlyToggle = document.getElementById('monthly-toggle');
    
    if (yearlyToggle && monthlyToggle) {
        yearlyToggle.addEventListener('click', function() {
            this.classList.remove('text-slate-400', 'hover:text-white');
            this.classList.add('bg-emerald-500', 'text-black');
            
            monthlyToggle.classList.remove('bg-emerald-500', 'text-black');
            monthlyToggle.classList.add('text-slate-400', 'hover:text-white');
        });
        
        monthlyToggle.addEventListener('click', function() {
            this.classList.remove('text-slate-400', 'hover:text-white');
            this.classList.add('bg-emerald-500', 'text-black');
            
            yearlyToggle.classList.remove('bg-emerald-500', 'text-black');
            yearlyToggle.classList.add('text-slate-400', 'hover:text-white');
        });
    }
});