
      var auth = btoa('admin:admin');

    var pageTotal = [];
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
        pageTotal = data.data;
          //  console.log( pageTotal)
        },
        error:function(data){
            console.log('request failed')
        }
    });

var Data1 = [];
     var Data2 = [];
     var Data3 = [];





for (i=0; i<pageTotal.length; i++) {
    Data1.push(pageTotal[i].population);
    Data2.push((pageTotal[i].gender['female percentage']*100).toFixed(2));
    Data3.push((pageTotal[i].gender['male percentage']*100).toFixed(2));
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
    // toolbox: {
    //     feature: {
    //         dataView: {show: true, readOnly: false},
    //         restore: {show: true},
    //         saveAsImage: {show: true}
    //     }
    // },
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
            data: Data3
        },
        {
            name: 'Female',
            type: 'bar',
            yAxisIndex: 1,
            data: Data2
        },
        {
            name: 'Total Population',
            type: 'line',
            yAxisIndex: 2,
            data: Data1
        }
    ]
};


    mychart1.setOption(option);
