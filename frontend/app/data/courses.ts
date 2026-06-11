export interface Course {
  id: number
  level: string
  color: string
  title: string
  hours: string
  lessons: string
  progress: number
  action?: string
  done?: boolean
}

export const courses: Course[] = [
  { id: 1, level: 'Базовый', color: 'blue', title: 'Основы финансовой безопасности', hours: '2 часа', lessons: '8 уроков', progress: 75, action: 'Продолжить' },
  { id: 2, level: 'Базовый', color: 'purple', title: 'Кредиты: что нужно знать', hours: '1.5 часа', lessons: '6 уроков', progress: 40, action: 'Продолжить' },
  { id: 3, level: 'Средний', color: 'middle', title: 'Криптовалюты: основы для инвестора', hours: '1.5 часа', lessons: '6 уроков', progress: 40, action: 'Продолжить' },
  { id: 4, level: 'Средний', color: 'green', title: 'Инвестиции для начинающих', hours: '3 часа', lessons: '10 уроков', progress: 0, action: 'Начать курс' },
  { id: 5, level: 'Базовый', color: 'red', title: 'Защита от мошенников', hours: '1 час', lessons: '5 уроков', progress: 100, action: 'Повторить', done: true },
  { id: 6, level: 'Базовый', color: 'red', title: 'Личный бюджет: от хаоса к системе', hours: '2 часа', lessons: '9 уроков', progress: 0, action: 'Повторить', done: true }
]
