if(typeof window !== 'undefined') {
    Element.prototype.matches = Element.prototype.matches ||
                                Element.prototype.matchesSelector ||
                                Element.prototype.mozMatchesSelector ||
                                Element.prototype.webkitMatchesSelector ||
                                Element.prototype.oMatchesSelector ||
                                Element.prototype.msMatchesSelector
}
