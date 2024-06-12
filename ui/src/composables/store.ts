
export function LocalStorage() {

  function setItem(key:string, value:string){
    window.localStorage.setItem(key,value)
  }

  function setItemJson(key:string, value:any){
    window.localStorage.setItem(key, JSON.stringify(value))
  }

  function getItem(key:string){
    const v = window.localStorage.getItem(key)
    if(v === null){ return null }
    try {
      return JSON.parse(v)
    } catch (e) {
      return v
    }
  }

  function deleteItem(key:string){
    window.localStorage.removeItem(key)
  }

  return {
    setItem, 
    setItemJson, 
    getItem,
    deleteItem
  };
}

