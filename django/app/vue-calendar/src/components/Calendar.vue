<template>
  <div>
    <!-- カレンダーヘッダー -->
    <div id="cal-header">
      <span class="header-arrow" @click="setLastMonth">＜</span>
      <span class="selected-month">{{ year }}.{{ month }}</span>
      <span class="header-arrow" @click="setNextMonth">＞</span>
    </div>
    <!-- カレンダーテーブル -->
    <table id="cal-main">
      <thead>
        <th v-for="dayname in weekdays" :key="dayname">{{ dayname}}</th>
      </thead>
      <tbody>
        <tr class="cal-day" v-for="(weekData, index) in calData" :key="index">
          <td v-for="(dayNum, index) in weekData" :key="index" @click="dateClick(dayNum)" :class="{'cal-today': isToday(dayNum), active: day === dayNum, isSaturday: index === 6, isSunday: index === 0, 'cal-holiday': isHoliday(dayNum)}">
            <span v-if="isToday(dayNum)">
              <strong>today</strong>
            </span>
            <span v-else>{{ dayNum }}</span>
          </td>
        </tr>
      </tbody>
    </table>
    <!-- 日付表示部分 -->
    <div class="holiday">
      <p>Today：{{ today }}</p>
      <button @click="setNextHoliday">Let's check next holiday!</button>
      <ul v-show="checkHoliday">
        <li>Next Holiday：{{nextHolidayDate}} ({{nextHolidayName}})</li>
        <transition>
          <li v-show="checkHoliday" class="check">
            There's
            <strong>{{termUntilNextHoliday}} days</strong> to next holiday...
          </li>
        </transition>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import { UPDATE_HOLIDAY } from '../store/mutation-types';
export default {
  data() {
    return {
      weekdays: ['Sun', 'Mon', 'Tue', 'Wed', 'Tur', 'Fri', 'Sat'],
      year: 2020,
      month: 10,
      day: -1,
      today: '',
      checkHoliday: false,
      nextHolidayObj: '',
      nextHolidayName: '',
      nextHolidayDate: '',
      termUntilNextHoliday: 0
    };
  },
  computed: {
    ...mapGetters(['holidayList']),
    calData() {
      const calData = []
      const firstWeekDay = new Date(this.year, this.month - 1, 1).getDay()
      const lastDay = new Date(this.year, this.month, 0).getDate()
      let dayNum = 1
      while (dayNum <= lastDay) {
        const weekData = []
        // 日曜～土曜の日付データを配列で作成
        for (let i = 0; i <= 6; i++) {
          if (calData.length === 0 && i < firstWeekDay) {
            // 初週の1日以前の曜日は空文字
            weekData[i] = ''
          } else if (lastDay < dayNum) {
            // 最終日以降の曜日は空文字
            weekData[i] = ''
          } else {
            // 通常の日付入力
            weekData[i] = dayNum
            dayNum++
          }
        }
        calData.push(weekData)
      }
      return calData
    }
  },
  created() {
    // 祝日データ取得
    this.$http(this.$httpHoliday)
      .then(response => {
        return response.json()
      })
      .then(data => {
        this[UPDATE_HOLIDAY](data)
      })
  },
  mounted() {
    // 今日の日付を文字列で算出
    const date = new Date()
    const y = date.getFullYear()
    const m = ('0' + (date.getMonth() + 1)).slice(-2)
    const d = ('0' + date.getDate()).slice(-2)
    this.year = y
    this.month = Number(m)
    this.today = y + '-' + m + '-' + d
  },
  methods: {
    ...mapActions([UPDATE_HOLIDAY]),
    setLastMonth() {
      if (this.month === 1) {
        this.year--
        this.month = 12
      } else {
        this.month--
      }
      this.day = -1
    },
    setNextMonth() {
      if (this.month === 12) {
        this.year++
        this.month = 1
      } else {
        this.month++
      }
      this.day = -1
    },
    dateClick(dayNum) {
      if (dayNum !== '') {
        this.day = dayNum
      }
    },
    isToday(day) {
      const date = this.setDateToString(day)
      if (this.today === date) {
        return true
      }
      return false
    },
    setDateToString(day) {
      // 日を年月日の文字列にして返す
      const date =
        this.year +
        '-' +
        String(this.month).padStart(2, '0') +
        '-' +
        String(day).padStart(2, '0')
      return date
    },
    isHoliday(day) {
      // Ajaxで取得した日と一致しているかチェック
      const date = this.setDateToString(day)
      for (const holiday in this.holidayList) {
        if (this.holidayList[holiday].date === date) {
          return true
        }
      }
      return false
    },
    calcTermDays(day1, day2) {
      // Dateオブジェクトの日数の差分を計算
      return (day2 - day1) / 86400000
    },
    calcNextHoliday() {
      // 次の祝日までの日数、および次の祝日のオブジェクトを返す
      for (const holiday in this.holidayList) {
        const holidayToDate = new Date(this.holidayList[holiday].date.split('-'))
        const todayToDate = new Date(this.today.split('-'))
        const termDays = this.calcTermDays(todayToDate, holidayToDate)
        if (termDays >= 0) {
          return [termDays, this.holidayList[holiday]]
        }
      }
    },
    setNextHoliday() {
      // 次の祝日の名前、日数をセット
      [this.termUntilNextHoliday, this.nextHolidayObj] = this.calcNextHoliday()
      this.nextHolidayName = this.nextHolidayObj.name
      this.nextHolidayDate = this.nextHolidayObj.date
      this.checkHoliday = true
    }
  }
};
</script>

<style scoped>
body {
  margin: 0;
}
#cal-header {
  font-size: 24px;
  padding: 0;
  text-align: center;
  margin-bottom: 10px;
  background-color: green;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: space-between;
}
#cal-header span {
  padding: 15px 20px;
  color: white;
  display: inline-block;
}
#cal-header .header-arrow {
  cursor: pointer;
}
#cal-main {
  font-size: 14px;
  line-height: 20px;
  table-layout: fixed;
  width: 100%;
  margin-bottom: 1rem;
  color: #212529;
  border-bottom: 1px solid #ddd;
  border-collapse: collapse;
}
#cal-main th {
  padding: 0;
  text-align: center;
  vertical-align: middle;
  font-weight: normal;
  color: #999;
}
#cal-main td {
  padding: 8px;
  text-align: center;
  vertical-align: middle;
  border-top: 1px solid #ddd;
}
.cal-today {
  background-color: #fcf8e3;
}
.cal-holiday {
  color: red;
}
.cal-day .active {
  background-color: #ffc9d7;
}
.cal-day .isSaturday {
  color: blue;
}
.cal-day .isSunday {
  color: red;
}
.holiday {
  position: absolute;
  top: 400px;
  right: 0;
  left: 0;
}
p {
  font-size: 30px;
}
li.check {
  font-family: "Eater", cursive;
}
button {
  margin: 30px auto 10px;
  width: 300px;
  font-size: 20px;
  padding: 5px;
  border: solid 1px #000;
  line-height: 30px;
  background: darkblue;
  color: #fff;
}
button:hover {
  cursor: pointer;
}
ul {
  list-style: none;
}
li {
  margin: 15px;
}
li > strong {
  color: red;
}
li {
  font-size: 30px;
}
.v-enter-active {
  transition: opacity 3s;
}
.v-enter-from {
  opacity: 0;
}
.v-enter-to {
  opacity: 1;
}
@media (min-width: 900px) {
  #cal-main,
  #cal-header {
    width: 900px;
    margin: auto;
  }
}
</style>
