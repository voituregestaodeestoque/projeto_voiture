const CACHE_NAME = "voiture_cache";

const arquivos = [
    "/",
    "../../templates/index.html",
];


self.addEventListener("install", function(event){
    event.waiUntil(
        caches.open(CACHE_NAME).then(function(cache){
            return cache.addAll(arquivos);
        })
    )
});