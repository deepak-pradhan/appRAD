import log from './utils/logger'; // Assuming the log utility is in this file

export async function handle({ event, resolve }) {

    const route = event.url

    log.bold(`👉 NEW REQUEST FROM: ${event.url.pathname}`)
    log.hooks(event.url.pathname)

    let beg = performance.now()
    const response = await resolve(event)
    let end = performance.now()

    let responseTime = end - beg
    if (responseTime > 2000) {
        console.log(`🐢 ${route} took ${responseTime.toFixed(2)} ms`)
    }

    if (responseTime < 1000) {
        console.log(`🚀 ${route} took ${responseTime.toFixed(2)} ms`)
    }

    log.bold(`👈 PAGE IS READY, HERE IS THE RESPONSE`)
    return response
}

// export async function handleError({ error, event })  {
//     // you can capture the `error` and `event` from the server
//     console.log(error)
  
//     return {
//       // don't show sensitive data to the user
//       message: 'Yikes! 💩',
//     }
//   }
  


   