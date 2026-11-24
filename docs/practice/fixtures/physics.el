import { QuantityVector, ampere, joule, kilogram, kilogramPerCubicMetre, metre, metrePerSecondSquared, newton, newtonSecond, ohm, pascal, second, volt } from "el:units/"
import { acceleration, constantForceImpulse, hydrostaticAbsolutePressure, hydrostaticPressureIncrease, ohmicCurrent } from "el:physics/"

let density = kilogramPerCubicMetre.of(1000)
let gravity = metrePerSecondSquared.of(9.81)
let depth = metre.of(2)
let surfacePressure = pascal.of(100000)
let increase = hydrostaticPressureIncrease(density, gravity, depth)
let pressure = hydrostaticAbsolutePressure(surfacePressure, density, gravity, depth)
console.stdout.writeLine("压力增量 ", increase.standardText())
console.stdout.writeLine("绝对压力 ", pressure.standardText())

@assign(mode: "copy")
class World {}

let WorldPlane: type = QuantityVector<frame: World, dimensions: 2>
let thrust = WorldPlane(@[newton.of(3), newton.of(4)])
let mass = kilogram.of(2)
let duration = second.of(2)
let displacement = WorldPlane(@[metre.of(2), metre.of(0)])
let accelerationVector = acceleration(thrust, mass)
let impulse = constantForceImpulse(thrust, duration)
let work = thrust.dot(displacement)
console.stdout.writeLine("纵向加速度 ", accelerationVector[1].inUnit(metrePerSecondSquared).standardText())
console.stdout.writeLine("冲量分量 ", impulse[0].valueIn(newtonSecond), ", ", impulse[1].valueIn(newtonSecond), " N·s")
console.stdout.writeLine("做功 ", work.inUnit(joule).standardText())

let current = ohmicCurrent(volt.of(-12), ohm.of(6))
console.stdout.writeLine("电流 ", current.inUnit(ampere).standardText())
