var auth = btoa('admin:admin');
var yXisdata=[];
function getPageTotalAndDataTotal() {
    var pageTotal = [];
    $.ajax({
        url:'http://172.26.129.233:5984/view_results(australia_tweets)/sa2_alcohol_senti_count',
        dataType:'json',
        async : false,
        xhrFields:{withCredentials:true},
        headers: {"Authorization": "Basic " + auth},
        crossDomain:true,
        success:function(data){
            pageTotal = data.rows;
            // console.log( pageTotal)
        },
        error:function(data){
            console.log('request failed')
        }
    });
    return pageTotal;
}

function getSuburbInfo() {
    var DBdata = [];
    $.ajax({
        url:'http://172.26.129.233:5984/view_results(australia_tweets)/suburb_info',
        dataType:'json',
        async : false,
        xhrFields:{withCredentials:true},
        headers: {"Authorization": "Basic " + auth},
        crossDomain:true,
        success:function(data){
            DBdata = data;
            // console.log(DBdata)
        },
        error:function(data){
            console.log('request failed')
        }
    });
    return DBdata;
}

var heatmapData = [];
var heatmapData1 = [];
var heatmapData2 = [];
var suburb_info = getSuburbInfo();
var lii = getPageTotalAndDataTotal();

for (i=0; (i+2)<lii.length; i++) {
    if (lii[i].key[0] == lii[i + 2].key[0]){
        var total = lii[i].value+lii[i+1].value+lii[i+2].value;
        if (total>10){
            heatmapData.push(((lii[i].value)/total * 100).toFixed(2));
            heatmapData1.push(((lii[i + 1].value)/total * 100).toFixed(2));
            heatmapData2.push(((lii[i + 2].value)/total * 100).toFixed(2));
            for (var key in suburb_info){
                if (key == lii[i].key[0]){
                    yXisdata.push(suburb_info[key]);
                    break;
                }
            } 
        }
        i += 2;
    }
}


option = {
        title: {
        text: 'The alcohol tweets sentiment of suburb',
        left: 'center'
    },
dataZoom: [
    {
        type: 'slider',
        show: true,
        yAxisIndex: [0],
        left: 'auto',
        start: 100, 
        end: 80,
        minSpan: 10,
        maxSpan: 40
    }
],
tooltip: {
    trigger: 'axis',
    axisPointer: {
        type: 'shadow'     //'line' | 'shadow'   　
    },
    formatter: '{b}<br />{a0}: {c0}%<br />{a1}: {c1}%<br />{a2}: {c2}%'
},
legend: {
    x:'center',      //left bottom center
    y:'bottom',     //left bottom center
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
    show: true,
    min: 0,
    max: 100
},
yAxis: {
    type: 'category',
    data: yXisdata
},
series: [
    {
        name: 'Neg',
        type: 'bar',
        stack: true,
        label: {
            show: true,
            position: 'right',
            formatter: '{c}%'
        },
        data: heatmapData
    },
    {
        name: 'Neu',
        type: 'bar',
        stack: true,
        label: {
            show: true,
            position: 'insideRight',
            formatter: '{c}%'
        },
        data: heatmapData1
    },
    {
        name: 'Pos',
        type: 'bar',
        stack: true,
        label: {
            show: true,
            position: 'insideRight',

                formatter: '{c}%'
        },
        data: heatmapData2
    }]
};
var ectest = echarts.init(document.getElementById("sentiment1"));
ectest.setOption(option);