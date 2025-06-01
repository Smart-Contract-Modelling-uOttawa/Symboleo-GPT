const { Asset } = require("symboleo-js-core");

class PerishableGood extends Asset {
  constructor(_name,quantity,quality,owner) {
    super()
    this._name = _name
    this.quantity = quantity
    this.quality = quality
    this.owner = owner
  }
}

module.exports.PerishableGood = PerishableGood
