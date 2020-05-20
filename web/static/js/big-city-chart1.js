                 var auth = btoa('admin:admin');
     function getPageTotalAndDataTotal() {
    var pageTotal = [];
            $.ajax({
        url:'http://172.26.129.233:5984/view_results(total_search)/city_sentiment_percent(total_search)',
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
        pageTotal = data.rows;
//console.log( pageTotal)
        },
        error:function(data){
            console.log('request failed')
        }
    });
    return pageTotal;
}
var heatmapData1 = [];
     var heatmapData11 = [];
     var heatmapData21 = [];
    var lii1 = getPageTotalAndDataTotal();

for (i=0; i<lii1.length; i++) {
    heatmapData1.push((lii1[i].value * 100).toFixed(2));
    heatmapData11.push((lii1[i + 1].value * 100).toFixed(2));
    heatmapData21.push((lii1[i + 2].value * 100).toFixed(2));
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
        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow'     // 默认为直线，可选为：'line' | 'shadow'
          　
        },

		formatter: '{b}<br />{a0}: {c0}%<br />{a1}: {c1}%<br />{a2}: {c2}%'

    },
    legend: {

                        x:'right',      //可设定图例在左、右、居中
        y:'bottom',     //可设定图例在上、下、居中
        padding:[0,5,5,0],
        data: ['Neg', 'Neu', 'Pos']
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
        data: ['Australian Capital Territory', 'Greater Adelaide', 'Greater Brisbane', 'Greater Darwin', 'Greater Hobart', 'Greater Melbourne', 'Greater Perth']
    },
    series: [
        {
            name: 'Neg',
            type: 'bar',
            stack: '总量',
            label: {
                show: true,
                position: 'insideRight',

                 formatter: '{c}%'
            },
            data: heatmapData1

        },
        {
            name: 'Neu',
            type: 'bar',
            stack: '总量',
            label: {
                show: true,
                position: 'insideRight',

                    formatter: '{c}%'
            },
            data: heatmapData11
        },
        {
            name: 'Pos',
            type: 'bar',
            stack: '总量',
            label: {
                show: true,
                position: 'insideRight',

                    formatter: '{c}%'
            },
            data: heatmapData21
        }
    ]
};

            ectest.setOption(option);