var Semantic_api = {
    _api_url: 'http://psn77-m.artgroup.local/',
    _get: function(url, params, cb) {
        if(typeof params == 'function') {
            cb = params;
            params = {};
        }
        var _url = this._api_url + url + '?' + $.param(params) + '&callback=?';

        console.log(_url)
        $.ajax({
            url: _url,
            success: function(data) {
                cb(data.results)
            },
            dataType: 'jsonp',
            error: console.error
        })
    },

    /*список всех статических вершин графа (name и href)*/
    getNodes: function(cb) {
        this._get('nodes/', cb)
    },

    /*статическая вершина графа с именем <name> (со всеми ее параметрами)*/
    getNode: function(node, cb) {
        this._get('nodes/'+node, cb)
        this._get('nodes/'+node, cb)
    },

    /*
     mode – режим поиска соседей, принимает два значения – поиск связей по ребрам (mode = 1, связь :LINKED) и поиск связей по отношению смежности (mode = 2, связь :CONNECTED). Обязательный параметр;
     depth – максимальное расстояние до соседа. Необязательный параметр, значение по умолчанию – 1;
     filters – типы вершин, которые следует вернуть в результате запроса. Допустимые значения –
        Concept, Link, Attribute, Parameter.
        Можно передавать несколько типов через запятую.
        Необязательный параметр, по умолчанию выдаются вершины любого типа;
    */
    getNeighbours: function(node, mode, depth, filters, cb) {
        this._get('nodes/'+node+'/neighbours', {
            mode: mode, //1
            depth: depth, //1
            filters: filters.join() //['Concept', 'Link', 'Attribute', 'Parameter']
        }, cb)
    },

    /*
     список объектов реального мира, связанных с этой вершиной.
    */
    getObjects: function(node, cb) {
        this._get('nodes/'+node+'/objects', cb)
    },

    /*
     список статических вершин, через которые проходит кратчайший путь между вершинами <source_name> и <destination_name>
       mode – режим поиска соседей, принимает два значения –
            поиск связей по ребрам (mode = 1, связь :LINKED) и
            поиск связей по отношению смежности (mode = 2, связь :CONNECTED).
            Обязательный параметр.
       filters – типы вершин, которые следует вернуть в результате запроса. Допустимые значения – Concept, Link, Attribute, Parameter. Можно передавать несколько типов через запятую. Необязательный параметр, по умолчанию выдаются вершины любого типа.
    */
    getShortestPath: function(from, to, mode, filters, cb) {
        //http://aplatonov:5000/nodes/Проект/shortest_path/Язык?mode=2&filters=Concept,Attribute
        this._get('nodes/'+from+'/shortest_path/'+to, {
            mode: mode,
            filters: ['Concept', 'Link', 'Attribute', 'Parameter'].join()
        }, cb)
    },
    /*
     список всех объектов графа (id и href)
    */
    getObject: function(id, cb) {
        this._get('objects/'+id, cb)
    },
    getObjectConnections: function(id, cb) {
        this._get('objects/'+id+'/connections', cb)
    }

}