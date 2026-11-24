import { centimetre, hour, kilometre, metre, second } from "el:units/"
import /^operator / from "el:units/"

let firstPart = centimetre.of(125)
let secondPart = metre.of(0.75)
let total = firstPart + secondPart
console.stdout.writeLine("总长 ", total.standardText())
console.stdout.writeLine("换成米 ", total.inUnit(metre).standardText())

let distance = metre.of(20)
let duration = second.of(2)
let speed = distance / duration
console.stdout.writeLine("平均速度 ", speed.valueIn(metre / second), " m/s")
console.stdout.writeLine("换成千米每小时 ", speed.valueIn(kilometre / hour), " km/h")
