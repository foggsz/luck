class PubSub{

    constructor(){
        this.subs = {}
    }

    addSub(event, func){
        this.subs[event]  = func
    }

    publish(event, args){
        if(this.subs[event]){
            this.subs[event](args)        }  
    }

    unSub(event){
        delete this.subs[event]
    }

}

let pubSUb = new PubSub()
pubSUb.addSub('haha', function(message){
    console.log(message)
})

pubSUb.publish("haha", 'sdsdsdds')
pubSUb.publish("haha", 'sdsdsddssdsd')