
export const option_pie = (title,seriesData) => {
  const legend = seriesData.map(o => o.name)
  return {
    title: {
      text: title,
      x: 'center'
    },
    tooltip: {
      // trigger: 'item',
      formatter: "{b}<br/>{c} ({d}%)"
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: legend
    },
    series: [{
      type: 'pie',
      radius: '55%',
      center: ['50%', '60%'],
      data: seriesData,
      itemStyle: {
        emphasis: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
}
export const option_bar = (title,res) => {
  if (res.code == 0) {
    const legend = res.data.map(o => o.name)
    const data = res.data.map(o => o.value)
    return {
      title: {
        text: title,
        subtext: '',
        x: 'center'
      },
      tooltip: {},
      legend: {
        orient: 'vertical',
        left: 'left',
        data: ['访问人数']
      },
      xAxis: {
        data: legend
      },
      yAxis: {},
      series: [{
        name: '访问人数',
        type: 'bar',
        barWidth: 40,
        data: data
      }]
    }
  }
}
export const option_line1 = (res) => {
  const dt = []
  const temperature_series = []
  const ph_series = []
  const dan_series = []
  const jia_series = []
  res.data.forEach(x => {
    dt.push(x.createTime)
    temperature_series.push(x.temperature)
    ph_series.push(x.ph)
    dan_series.push(x.dan)
    jia_series.push(x.jia)
  })

  return {
    color: ['#40c9c6', '#36a3f7', '#f4516c'],
    tooltip: {
      trigger: 'axis',
      position: function(pt) {
        return [pt[0], '10%'];
      }
    },
    title: {
      text: '历史数据曲线',
    },
    legend: {
      data: ['温度', 'ph值', '氮肥含量', '钾肥含量']
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dt
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: '温度',
        type: 'line',
        smooth: true,
        data: temperature_series
      },
      {
        name: 'ph值',
        type: 'line',
        smooth: true,
        data: ph_series
      },
      {
        name: '氮肥含量',
        type: 'line',
        smooth: true,
        data: dan_series
      },
      {
        name: '钾肥含量',
        type: 'line',
        smooth: true,
        data: jia_series
      },
    ]
  };
}
