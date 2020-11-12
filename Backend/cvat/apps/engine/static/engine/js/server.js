/* exported encodeFilePathToURI */

function encodeFilePathToURI(path) {
    return path.split('/').map(x => encodeURIComponent(x)).join('/');
}
