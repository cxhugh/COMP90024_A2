
      var auth = btoa('admin:admin');

    var char3 = [];
            $.ajax({
        url:'http://172.26.129.233:5984/aurin_result/gender',
        dataType:'json',
       async : false,
                xhrFields:{
      withCredentials:true
            },
       headers: {
        "Authorization": "Basic " + auth
    },
            crossDomain:true,

        success:function(data){
        char3 = data.data;
          //  console.log( pageTotal)
        },
        error:function(data){
            console.log('request failed')
        }
    });

var char3Data1 = [];
var char3Data2 = [];
var char3Data3 = [];





for (i=0; i<char3.length; i++) {
    char3Data1.push(char3[i].population);
    char3Data2.push((char3[i].gender['female percentage']*100).toFixed(2));
    char3Data3.push((char3[i].gender['male percentage']*100).toFixed(2));
}



















var mychart1 = echarts.init(document.getElementById("charts3"));

var colors = ['#5793f3', '#d14a61', '#675bba'];

option = {
    color: colors,

    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross'
        }
    },
    grid: {
        right: '20%'
    },

    legend: {
        data: ['Male', 'Female', 'Total Number']
    },
    xAxis: [
        {
            type: 'category',
            axisTick: {
                alignWithLabel: true
            },
            data: ['NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS','NT','ACT']
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: 'Male',
            min: 0,
            max: 100,
            position: 'right',
            axisLine: {
                lineStyle: {
                    color: colors[0]
                }
            },
            axisLabel: {
                formatter: '{value} %'
            }
        },
        {
            type: 'value',
            name: 'Female',
            min: 0,
            max: 100,
            position: 'right',
            offset: 80,
            axisLine: {
                lineStyle: {
                    color: colors[1]
                }
            },
            axisLabel: {
                formatter: '{value} %'
            }
        },
        {
            type: 'value',
            name: 'Total Number',
            min: 100000,
            max: 10000000,
            position: 'left',
            axisLine: {
                lineStyle: {
                    color: colors[2]
                }
                },
            axisLabel: {
                formatter: '{value} '
            }
        }
    ],
    series: [
        {
            name: 'Male',
            type: 'bar',
            data: char3Data3
        },
        {
            name: 'Female',
            type: 'bar',
            yAxisIndex: 1,
            data: char3Data2
        },
        {
            name: 'Total Population',
            type: 'line',
            yAxisIndex: 2,
            data: char3Data1
        }
    ]
};


    mychart1.setOption(option);
