      var auth = btoa('admin:admin');

    var char2 = [];
            $.ajax({
        url:'http://172.26.129.233:5984/aurin_result/age_number',
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
        char2 = data.data;
          //  console.log( pageTotal)
        },
        error:function(data){
            console.log('request failed')
        }
    });

var char2Data11 = ['0~14 years'];
     var char2Data22 = ['15~24 years'];
     var char2Data33 = ['25~49 years'];
     var char2Data44 = ['50~74 years'];
     var char2Data55 = ['75~ years'];



for (i=0; i<char2.length; i++) {
    char2Data11.push(char2[i].age['0 to 14'] );
    char2Data22.push(char2[i].age['15 to 24']  );
    char2Data33.push(char2[i].age['25 to 49']  );
    char2Data44.push(char2[i].age['50 to 74']  );
    char2Data55.push(char2[i].age['75 and over']  );
}








setTimeout(function () {


         var mychart = echarts.init(document.getElementById("charts2"));

    option = {
        legend: {},
        tooltip: {
            trigger: 'axis',
            showContent: false
        },
        dataset: {
            source: [
                ['product', 'NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS','NT','ACT'],
                char2Data11,
                char2Data22,
                char2Data33,
                char2Data44,
                char2Data55
            ]
        },
        xAxis: {type: 'category'},
        yAxis: {gridIndex: 0},
        grid: {top: '55%'},
        series: [
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {
                type: 'pie',
                id: 'pie',
                radius: '30%',
                center: ['50%', '25%'],
                label: {
                    formatter: '{b}: {@QLD} ({d}%)'
                },
                encode: {
                    itemName: 'product',
                    value: 'QLD',
                    tooltip: 'QLD'
                }
            }
        ]
    };

    mychart.on('updateAxisPointer', function (event) {
        var xAxisInfo = event.axesInfo[0];
        if (xAxisInfo) {
            var dimension = xAxisInfo.value + 1;
            mychart.setOption({
                series: {
                    id: 'pie',
                    label: {
                        formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                    },
                    encode: {
                        value: dimension,
                        tooltip: dimension
                    }
                }
            });
        }
    });

    mychart.setOption(option);

});