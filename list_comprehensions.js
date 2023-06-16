var listComprehension = function(str) {
  let arr = []
  
  str = str.slice(1, str.length-1)
  let regexp = /for\s+(\w+)\s+in\s+(.*)/
  let matched = str.match(regexp)
  let body = str.slice(0, matched.index)
  let id = matched[1]
  let list = eval(matched[2])
  
  if(matched == null) { // null == matched, !matched
    throw new Error('Syntax Error')
  }
  
  for(let x of list) {
    this[id] = x
    arr.push(eval(body))
    
  }
  return arr
  
}
