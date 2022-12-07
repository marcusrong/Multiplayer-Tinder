function get_data(){
    let url = fetch("http://172.16.60.27:8080/data.json");
    fetch(url)
        .then(res => res.json())
        .then(out =>
            console.log('Checkout this JSON! ', out))
        .catch(err => { throw err });
}


const socket = new WebSocket('ws://127.0.0.1:8080');

socket.addEventListener('open', function(event){
    socket.send('Connection established')
});

socket.addEventListener('message', function(event){
    console.log(event.data)
});

const contactServer = ()=>{
    socket.send('Initialyse')
}



