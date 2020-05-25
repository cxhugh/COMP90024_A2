var auth = btoa('admin:admin');

var char1 = [];
$.ajax({
        url:'http://172.26.134.56:5984/view_results(australia_tweets)/city_alcohol_senti_percent',
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
                 char1 = data.rows;
            //console.log( pageTotal)
        },
        error:function(data){
            console.log('request failed')
        }
});

var char1Data1 = [];
var char1Data11 = [];
var char1Data21 = [];


for (i=0; i<char1.length; i++) {
    char1Data1.push((char1[i].value * 100).toFixed(2));
    char1Data11.push((char1[i + 1].value * 100).toFixed(2));
    char1Data21.push((char1[i + 2].value * 100).toFixed(2));
    i += 2;
}

var ectest = echarts.init(document.getElementById("charts1"));
option = {
            title: {
            text: 'The sentiment of city',
             left: 'center'
              },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
          　
        },

		formatter: '{b}<br />{a0}: {c0}%<br />{a1}: {c1}%<br />{a2}: {c2}%'

    },
    legend: {

           x:'right',
        y:'bottom',
        padding:[0,5,5,0],
        data: ['Negative', 'Neutral', 'Positive']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        show: false
    },
    yAxis: {
        type: 'category',
        data: ['Australian Capital Territory', 'Greater Adelaide', 'Greater Brisbane', 'Greater Darwin', 'Greater Hobart', 'Greater Melbourne', 'Greater Perth', 'Greater Sydney']
    },
    series: [
        {
            name: 'Negative',
            type: 'bar',
            stack: 'total',
            label: {
                show: true,
                position: 'insideRight',

                 formatter: '{c}%'
            },
            data: char1Data1

        },
        {
            name: 'Neutral',
            type: 'bar',
            stack: 'total',
            label: {
                show: true,
                position: 'insideRight',

                    formatter: '{c}%'
            },
            data: char1Data11
        },
        {
            name: 'Positive',
            type: 'bar',
            stack: 'total',
            label: {
                show: true,
                position: 'insideRight',

                    formatter: '{c}%'
            },
            data: char1Data21
        }
    ]
};

            ectest.setOption(option);