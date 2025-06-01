const { PerishableGood } = require("./PerishableGood.js");

class Meat extends PerishableGood {
  constructor(_name,quantity,quality,owner) {
    super(_name,quantity,quality,owner)
  }
}

module.exports.Meat = Meat
