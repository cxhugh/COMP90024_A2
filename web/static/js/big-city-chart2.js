      var auth = btoa('admin:admin');
     function getPageTotalAndDataTotal() {
    var pageTotal = [];
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
        pageTotal = data.data;
          //  console.log( pageTotal)
        },
        error:function(data){
            console.log('request failed')
        }
    });
    return pageTotal;
}
var Data1 = ['0~14 years'];
     var Data2 = ['15~24 years'];
     var Data3 = ['25~49 years'];
     var Data4 = ['50~74 years'];
     var Data5 = ['75~ years'];

    var lii = getPageTotalAndDataTotal();


for (i=0; i<lii.length; i++) {
    Data1.push(lii[i].age['0 to 14'] );
    Data2.push(lii[i].age['15 to 24']  );
    Data3.push(lii[i].age['25 to 49']  );
    Data4.push(lii[i].age['50 to 74']  );
    Data5.push(lii[i].age['75 and over']  );
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
                Data1,
                Data2,
                Data3,
                Data4,
                Data5
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