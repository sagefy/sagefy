/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	document.addEventListener('DOMContentLoaded', __webpack_require__(1).go);

/***/ },
/* 1 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch,
	    bind = _require.bind,
	    setReducer = _require.setReducer;

	var reducer = __webpack_require__(3);
	var init = __webpack_require__(43);
	var cookie = __webpack_require__(8);

	var _require2 = __webpack_require__(72),
	    route = _require2.route;

	var _require3 = __webpack_require__(76),
	    startGoogleAnalytics = _require3.startGoogleAnalytics,
	    trackEvent = _require3.trackEvent;

	var indexView = __webpack_require__(77);

	var _require4 = __webpack_require__(7),
	    setTitle = _require4.setTitle;

	startGoogleAnalytics

	// Require all tasks
	();__webpack_require__(188

	// Require all broker events
	);__webpack_require__(208);

	__webpack_require__(209);
	__webpack_require__(210);
	__webpack_require__(211);
	__webpack_require__(212);
	__webpack_require__(213);
	__webpack_require__(214);
	__webpack_require__(215);
	__webpack_require__(216);

	__webpack_require__(217);
	__webpack_require__(218);
	__webpack_require__(219);
	__webpack_require__(220);
	__webpack_require__(221);
	__webpack_require__(222);
	__webpack_require__(223);
	__webpack_require__(224);
	__webpack_require__(225);
	__webpack_require__(226);
	__webpack_require__(227);
	__webpack_require__(228);
	__webpack_require__(229);
	__webpack_require__(230);
	__webpack_require__(231);
	__webpack_require__(232);
	__webpack_require__(233);
	__webpack_require__(234

	// Log all recorder events to the console and analytics
	);function logAllActions() {
	    bind(function (state, action) {
	        console.log(action.type, action, state // eslint-disable-line
	        );
	    });
	}

	function trackAllActions() {
	    bind(function (state, action) {
	        trackEvent(action);
	    });
	}

	function updateTitle() {
	    bind(function (state, action) {
	        if (action.type === 'SET_ROUTE') {
	            setTitle(action.title);
	        }
	    });
	}

	// Start up the application
	function go() {
	    logAllActions();
	    trackAllActions();
	    updateTitle();
	    setReducer(reducer);
	    dispatch({
	        type: 'SET_CURRENT_USER_ID',
	        currentUserID: cookie.get('currentUserID')
	    });
	    route(window.location.pathname + window.location.search);
	    init({
	        view: indexView,
	        el: document.body
	    });
	}

	module.exports = { go: go, logAllActions: logAllActions, trackAllActions: trackAllActions };

/***/ },
/* 2 */
/***/ function(module, exports) {

	'use strict';

	var listeners = [];
	var state = typeof window === 'undefined' ? {} : window.preload || {};
	var reducer = function reducer() {};
	function bind(fn) {
	    listeners.push(fn);
	}
	function setReducer(fn) {
	    reducer = fn;
	}
	function dispatch() {
	    var action = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : { type: '' };

	    state = reducer(state, action);
	    listeners.forEach(function (fn) {
	        return fn(state, action);
	    });
	}
	function getState() {
	    return state;
	}
	function resetState() {
	    state = reducer({}, { type: '' });
	}
	module.exports = { setReducer: setReducer, bind: bind, dispatch: dispatch, getState: getState, resetState: resetState };

/***/ },
/* 3 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable global-require */

	function combineReducers(reducerMap) {
	    var keys = Object.keys(reducerMap);
	    return function combinedReducer() {
	        var prevState = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	        var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	        return keys.reduce(function (newState, key) {
	            newState[key] = reducerMap[key](prevState[key], action);
	            return newState;
	        }, {});
	    };
	}

	// TODO-3 change file names to camelcase to match other files

	module.exports = combineReducers({
	    cardFeedback: __webpack_require__(4),
	    cardResponse: __webpack_require__(5),
	    cardVersions: __webpack_require__(6),
	    cards: __webpack_require__(11),
	    chooseUnit: __webpack_require__(12),
	    currentTreeUnit: __webpack_require__(13),
	    currentUserID: __webpack_require__(14),
	    create: __webpack_require__(15),
	    errors: __webpack_require__(16),
	    follows: __webpack_require__(17),
	    formData: __webpack_require__(18),
	    learnCards: __webpack_require__(19),
	    menu: __webpack_require__(20),
	    next: __webpack_require__(21),
	    notices: __webpack_require__(22),
	    passwordPageState: __webpack_require__(23),
	    recommendedSubjects: __webpack_require__(24),
	    route: __webpack_require__(25),
	    routeQuery: __webpack_require__(26),
	    routeTitle: __webpack_require__(27),
	    searchQuery: __webpack_require__(28),
	    searchResults: __webpack_require__(29),
	    sending: __webpack_require__(30),
	    subjectTrees: __webpack_require__(31),
	    subjectVersions: __webpack_require__(32),
	    subjects: __webpack_require__(33),
	    topicPosts: __webpack_require__(34),
	    topicPostVersions: __webpack_require__(35),
	    topics: __webpack_require__(36),
	    unitLearned: __webpack_require__(37),
	    unitVersions: __webpack_require__(38),
	    units: __webpack_require__(39),
	    users: __webpack_require__(40),
	    userAvatars: __webpack_require__(41),
	    userSubjects: __webpack_require__(42)
	});

/***/ },
/* 4 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function cardFeedback() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'RESET_CARD_FEEDBACK') {
	        return '';
	    }
	    if (action.type === 'SET_CARD_FEEDBACK') {
	        return action.feedback;
	    }
	    return state;
	};

/***/ },
/* 5 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function cardResponse() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'RESET_CARD_RESPONSE') {
	        return {};
	    }
	    if (action.type === 'SET_CARD_RESPONSE') {
	        return action.response;
	    }
	    return state;
	};

/***/ },
/* 6 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(7),
	    mergeArraysByKey = _require.mergeArraysByKey;

	var _require2 = __webpack_require__(9),
	    shallowCopy = _require2.shallowCopy;

	module.exports = function cardVersions() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_CARD_VERSIONS') {
	        var versions = state[action.entity_id] || [];
	        versions = mergeArraysByKey(versions, action.versions, 'id' // id is the version id
	        );
	        state = shallowCopy(state);
	        state[action.entity_id] = versions;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 7 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

	function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

	/*
	Auxiliaries are utlity functions that are specific to Sagefy.
	*/

	var cookie = __webpack_require__(8);

	var _require = __webpack_require__(9

	// Determine if the user is logged in
	),
	    extend = _require.extend,
	    copy = _require.copy,
	    isString = _require.isString,
	    isArray = _require.isArray;

	var isLoggedIn = function isLoggedIn() {
	    return cookie.get('logged_in') === '1';
	};

	// Capitalizes the first letter of a string
	var ucfirst = function ucfirst() {
	    var str = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
	    return str.charAt(0).toUpperCase() + str.slice(1

	    // Replaces dashes and spaces with underscores, ready to be used in an URL
	    );
	};var underscored = function underscored(str) {
	    return str.replace(/[-\s]+/g, '_').toLowerCase

	    // From Handlebars
	    ();
	};var escape = function escape(str) {
	    var chars = {
	        '&': '&amp;',
	        '<': '&lt;',
	        '>': '&gt;',
	        '"': '&quot;',
	        "'": '&#x27;',
	        '`': '&#x60;'
	    };

	    return str.toString().replace(/[&<>"'`]/g, function (char) {
	        return chars[char];
	    });
	};

	// From http://ejohn.org/files/pretty.js
	// TODO-3 move copy to content directory
	var timeAgo = function timeAgo(str) {
	    var diff = new Date().getTime() - new Date(str).getTime();
	    var days = Math.floor(diff / (24 * 60 * 60 * 1000));
	    var hours = Math.floor(diff / (60 * 60 * 1000));
	    var minutes = Math.floor(diff / (60 * 1000));
	    if (days > 1) return days + ' days ago';
	    if (days === 1) return 'Yesterday';
	    if (hours > 1) return hours + ' hours ago';
	    if (hours === 1) return '1 hour ago';
	    if (minutes > 1) return minutes + ' minutes ago';
	    if (minutes === 1) return '1 minute ago';
	    return 'Just now';
	};

	// Return a variable friendly name of the title.
	var slugify = function slugify(s) {
	    return s.toLowerCase().replace(/[-\s]+/g, '_'

	    // Set the page title.
	    );
	};var setTitle = function setTitle() {
	    var title = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'FIX ME';

	    title = title + ' \u2013 Sagefy';
	    if (typeof document !== 'undefined' && document.title !== title) {
	        document.title = title;
	    }
	};

	// Wait for function to stop being called for `delay`
	// milliseconds, and then finally call the real function.
	var debounce = function debounce(fn, delay) {
	    var timer = null;
	    return function debounceInternal() {
	        var _this = this;

	        for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
	            args[_key] = arguments[_key];
	        }

	        clearTimeout(timer);
	        timer = setTimeout(function () {
	            return fn.apply(_this, args);
	        }, delay);
	    };
	};

	// Determine if a given path matches this router.
	// Returns either false or array, where array is matches parameters.
	var matchesRoute = function matchesRoute(docPath, viewPath) {
	    if (!docPath) {
	        return false;
	    }
	    docPath = docPath.split('?')[0]; // Only match the pre-query params
	    if (isString(viewPath)) {
	        viewPath = new RegExp('^' + viewPath.replace(/\{([\d\w\-_\$]+)\}/g, '([^/]+)') + '$');
	    }
	    var match = docPath.match(viewPath);
	    return match ? match.slice(1) : false;
	};

	var valuefy = function valuefy(value) {
	    if (typeof value === 'undefined') return undefined;
	    if (value === 'true') return true;
	    if (value === 'false') return false;
	    if (value === 'null') return null;
	    if (value.match(/^\d+\.\d+$/)) return parseFloat(value);
	    if (value.match(/^\d+$/)) return parseInt(value);
	    return decodeURIComponent(value);
	};

	var truncate = function truncate(str, len) {
	    if (str.length <= len) return str;
	    return str.slice(0, len) + '...';
	};

	var compact = function compact(A) {
	    var _ = [];
	    var _iteratorNormalCompletion = true;
	    var _didIteratorError = false;
	    var _iteratorError = undefined;

	    try {
	        for (var _iterator = A[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
	            var a = _step.value;

	            if (a) {
	                _.push(a);
	            }
	        }
	    } catch (err) {
	        _didIteratorError = true;
	        _iteratorError = err;
	    } finally {
	        try {
	            if (!_iteratorNormalCompletion && _iterator.return) {
	                _iterator.return();
	            }
	        } finally {
	            if (_didIteratorError) {
	                throw _iteratorError;
	            }
	        }
	    }

	    return _;
	};

	var mergeArraysByKey = function mergeArraysByKey(A, B) {
	    var key = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 'id';

	    var a = 0;
	    var b = 0;
	    var C = [];

	    A = compact(A);
	    B = compact(B);

	    while (a < A.length) {
	        var b2 = b;
	        var found = false;

	        while (b2 < B.length) {
	            if (A[a][key] === B[b2][key]) {
	                while (b <= b2) {
	                    C.push(B[b]);
	                    b++;
	                }
	                found = true;
	                break;
	            }
	            b2++;
	        }

	        if (!found) {
	            C.push(A[a]);
	        }

	        a++;
	    }

	    while (b < B.length) {
	        C.push(B[b]);
	        b++;
	    }

	    return C;
	};

	// Returns an object of the fields' value
	var getFormValues = function getFormValues(form) {
	    var data = {};
	    var forEach = function forEach(nl, fn) {
	        return Array.prototype.forEach.call(nl, fn);
	    };
	    forEach(form.querySelectorAll(['input[type="text"]', 'input[type="email"]', 'input[type="password"]', 'input[type="hidden"]', 'textarea'].join(', ')), function (el) {
	        data[el.name] = valuefy(el.value);
	    });
	    forEach(form.querySelectorAll('[type=radio]'), function (el) {
	        if (el.checked) {
	            data[el.name] = valuefy(el.value);
	        }
	    });
	    forEach(form.querySelectorAll('[type=checkbox]'), function (el) {
	        data[el.name] = data[el.name] || [];
	        if (el.checked) {
	            data[el.name].push(valuefy(el.value));
	        }
	    });
	    return data;
	};

	// Given a forms values as an object, parse any fields with `.`
	// in them to create a save-able object for the service
	var parseFormValues = function parseFormValues(data) {
	    var output = {};

	    var _loop = function _loop(key) {
	        var value = data[key];
	        if (key.indexOf('.') === -1) {
	            output[key] = value;
	        } else {
	            var prev = output;
	            var next = void 0;
	            var names = key.split('.').map(function (n) {
	                return (/^\d+$/.test(n) ? parseInt(n) : n
	                );
	            });
	            names.forEach(function (name, i) {
	                if (i === names.length - 1) {
	                    prev[name] = value;
	                } else {
	                    next = names[i + 1];
	                    if (typeof next === 'string') {
	                        prev[name] = prev[name] || {};
	                    } else if (typeof next === 'number') {
	                        prev[name] = prev[name] || [];
	                    }
	                    prev = prev[name];
	                }
	            });
	        }
	    };

	    for (var key in data) {
	        _loop(key);
	    }
	    return output;
	};

	// Validate the entry with the given ID against the schema.
	// Returns a list of errors.
	// Use this method for any sort of `create` or `update` call.
	var validateFormData = function validateFormData(data, schema, fields) {
	    var errors = [];(fields || Object.keys(schema)).forEach(function (fieldName) {
	        schema[fieldName].validations.forEach(function (fn) {
	            var error = void 0;
	            if (isArray(fn)) {
	                error = fn[0].apply(fn, [data[fieldName]].concat(_toConsumableArray(fn.slice(1))));
	            } else {
	                error = fn(data[fieldName]);
	            }
	            if (error) {
	                errors.push({
	                    name: fieldName,
	                    message: error
	                });
	                return;
	            }
	        });
	    });
	    return errors;
	};

	// Given a schema, fields, errors, formData, and sending boolean (optional)
	// create a list of fields with all the data needed to create the form
	// correctly.
	function createFieldsData(_ref) {
	    var schema = _ref.schema,
	        fields = _ref.fields,
	        _ref$errors = _ref.errors,
	        errors = _ref$errors === undefined ? [] : _ref$errors,
	        _ref$formData = _ref.formData,
	        formData = _ref$formData === undefined ? {} : _ref$formData,
	        _ref$sending = _ref.sending,
	        sending = _ref$sending === undefined ? false : _ref$sending;

	    fields = copy(fields);

	    fields.forEach(function (field, i) {
	        fields[i] = extend({}, schema[field.name] || {}, field);
	    });

	    if (errors) {
	        errors.forEach(function (error) {
	            var field = fields.filter(function (f) {
	                return f.name === error.name;
	            });
	            if (field) {
	                field = field[0];
	            }
	            if (field) {
	                field.error = error.message;
	            }
	        });
	    }

	    Object.keys(formData).forEach(function (name) {
	        var value = formData[name];
	        // All of this for the list input type
	        var matches = name.match(/^(.*)\.(\d+)\.(.*)$/);
	        if (matches) {
	            var _matches = _slicedToArray(matches, 4),
	                pre = _matches[1],
	                index = _matches[2],
	                col = _matches[3];

	            var field = fields.filter(function (f) {
	                return f.name === pre;
	            });
	            if (field) {
	                field = field[0];
	            }
	            if (field) {
	                field.value = field.value || [];
	                field.value[index] = field.value[index] || {};
	                field.value[index][col] = value;
	            }
	            // For every other kind of field...
	        } else {
	            var _field = fields.filter(function (f) {
	                return f.name === name;
	            });
	            if (_field) {
	                _field = _field[0];
	            }
	            if (_field) {
	                _field.value = value;
	            }
	        }
	    });

	    if (sending) {
	        var field = fields.filter(function (f) {
	            return f.type === 'submit';
	        });
	        if (field) {
	            field = field[0];
	        }
	        if (field) {
	            field.disabled = true;
	        }
	    }

	    return fields;
	}

	function findGlobalErrors(_ref2) {
	    var fields = _ref2.fields,
	        errors = _ref2.errors;

	    var fieldNames = fields.map(function (field) {
	        return field.name;
	    });
	    return errors.filter(function (error) {
	        return !error.name || fieldNames.indexOf(error.name) === -1;
	    });
	}

	var prefixObjectKeys = function prefixObjectKeys(prefix, obj) {
	    var next = {};
	    Object.keys(obj).forEach(function (name) {
	        var value = obj[name];
	        next[prefix + name] = value;
	    });
	    return next;
	};

	module.exports = {
	    isLoggedIn: isLoggedIn,
	    ucfirst: ucfirst,
	    underscored: underscored,
	    escape: escape,
	    timeAgo: timeAgo,
	    slugify: slugify,
	    setTitle: setTitle,
	    debounce: debounce,
	    matchesRoute: matchesRoute,
	    truncate: truncate,
	    mergeArraysByKey: mergeArraysByKey,
	    valuefy: valuefy,

	    getFormValues: getFormValues,
	    parseFormValues: parseFormValues,
	    validateFormData: validateFormData,
	    createFieldsData: createFieldsData,
	    findGlobalErrors: findGlobalErrors,

	    prefixObjectKeys: prefixObjectKeys,
	    compact: compact
	};

/***/ },
/* 8 */
/***/ function(module, exports) {

	'use strict';

	// Read, create, update, and delete cookies.
	var encode = encodeURIComponent;
	var decode = decodeURIComponent;

	// Read and parse a cookie key/value.
	var read = function read(s) {
	    if (s.indexOf('"') === 0) {
	        s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
	    }
	    return decode(s.replace(/\+/g, ' '));
	};

	// Get the cookie value at a particular key.
	var get = function get(key) {
	    if (typeof document === 'undefined') {
	        return null;
	    }
	    var name = key + '=';
	    var cookies = document.cookie.split(';');
	    var _iteratorNormalCompletion = true;
	    var _didIteratorError = false;
	    var _iteratorError = undefined;

	    try {
	        for (var _iterator = cookies[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
	            var c = _step.value;

	            c = c.trim();
	            if (c.indexOf(name) === 0) {
	                return read(c.substring(name.length));
	            }
	        }
	    } catch (err) {
	        _didIteratorError = true;
	        _iteratorError = err;
	    } finally {
	        try {
	            if (!_iteratorNormalCompletion && _iterator.return) {
	                _iterator.return();
	            }
	        } finally {
	            if (_didIteratorError) {
	                throw _iteratorError;
	            }
	        }
	    }

	    return null;
	};

	// Set the cookie value at a specific key.
	var set = function set(key, value) {
	    var time = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 31556926;

	    if (typeof document === 'undefined') {
	        return;
	    }
	    if (value === null || value === undefined) {
	        return;
	    }
	    document.cookie = [encode(key), '=', '' + value, ';path=/', ';max-age=' + time].join('');
	    return document.cookie;
	};

	// Remove the cookie value at a specific key.
	var unset = function unset(key) {
	    return set(key, '', -1);
	};

	module.exports = {
	    read: read,
	    get: get,
	    set: set,
	    unset: unset
	};

/***/ },
/* 9 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/*
	Utilities are one-off functions that are used throughout the framework.
	*/
	var util = {}

	// Test for types.
	;['Object', 'Array', 'Function', 'Date', 'String', 'RegExp'].forEach(function (type) {
	    util['is' + type] = function (a) {
	        return Object.prototype.toString.call(a) === '[object ' + type + ']';
	    };
	});

	util.isUndefined = function (a) {
	    return typeof a === 'undefined';
	};

	// http://stackoverflow.com/a/9716488
	util.isNumber = function (n) {
	    return !isNaN(parseFloat(n)) && isFinite(n);
	};

	var objectConstructor = {}.constructor;

	// Add the properties of the injects into the target.
	util.extend = function (target) {
	    for (var _len = arguments.length, injects = Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
	        injects[_key - 1] = arguments[_key];
	    }

	    injects.forEach(function (inject) {
	        Object.keys(inject).forEach(function (prop) {
	            var val = inject[prop];
	            if (util.isUndefined(val)) {
	                return;
	            }
	            if (util.isDate(val)) {
	                target[prop] = new Date(val);
	            } else if (util.isArray(val)) {
	                if (!util.isArray(target[prop])) {
	                    target[prop] = [];
	                }
	                target[prop] = util.extend([], target[prop], val);
	            } else if (util.isObject(val) && val.constructor === objectConstructor) {
	                if (!util.isObject(target[prop])) {
	                    target[prop] = {};
	                }
	                target[prop] = util.extend({}, target[prop], val);
	            } else {
	                target[prop] = val;
	                // number, boolean, string, regexp, null, function
	            }
	        });
	    });
	    return target;
	};

	// Makes a copy of the array or object.
	util.copy = function (obj) {
	    if (util.isObject(obj)) {
	        return util.extend({}, obj);
	    }
	    if (util.isArray(obj)) {
	        return util.extend([], obj);
	    }
	    if (util.isDate(obj)) {
	        return new Date(obj);
	    }
	    return obj;
	};

	util.shallowCopy = function (obj) {
	    return Object.keys(obj).reduce(function (next, key) {
	        next[key] = obj[key];
	        return next;
	    }, {});
	};

	// Try to parse a string as JSON, otherwise just return the string.
	util.parseJSON = function (str) {
	    try {
	        return JSON.parse(str);
	    } catch (e) {
	        return str;
	    }
	};

	// Find the closest element matching the given selector.
	__webpack_require__(10);

	util.closest = function (element, selector) {
	    var top = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : document.body;

	    while (!element.matches(selector)) {
	        element = element.parentNode;
	        if (element === top) {
	            return null;
	        }
	    }
	    return element;
	};

	// Convert an object to a query string for GET requests.
	util.parameterize = function (obj) {
	    obj = util.copy(obj);
	    var pairs = [];
	    for (var key in obj) {
	        var value = obj[key];
	        pairs.push(encodeURIComponent(key) + '=' + encodeURIComponent(value));
	    }
	    return pairs.join('&').replace(/%20/g, '+');
	};

	util.convertDataToGet = function (url, data) {
	    url += url.indexOf('?') > -1 ? '&' : '?';
	    url += util.parameterize(util.extend(data || {}, { _: +new Date() // Cachebreaker
	    }));
	    return url;
	};

	module.exports = util;

/***/ },
/* 10 */
/***/ function(module, exports) {

	'use strict';

	if (typeof window !== 'undefined') {
	    Element.prototype.matches = Element.prototype.matches || Element.prototype.matchesSelector || Element.prototype.mozMatchesSelector || Element.prototype.webkitMatchesSelector || Element.prototype.oMatchesSelector || Element.prototype.msMatchesSelector;
	}

/***/ },
/* 11 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(9),
	    shallowCopy = _require.shallowCopy;

	module.exports = function cards() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_CARD') {
	        state = shallowCopy(state);
	        state[action.card.entity_id] = action.card;
	        return state;
	    }
	    if (action.type === 'GET_CARD_SUCCESS') {
	        var card = action.card;['card_parameters'].forEach(function (r) {
	            card[r] = action[r];
	        });
	        card.relationships = [{
	            kind: 'belongs_to',
	            entity: action.unit
	        }];['requires', 'required_by'].forEach(function (r) {
	            return action[r].forEach(function (e) {
	                return card.relationships.push({
	                    kind: r,
	                    entity: e
	                });
	            });
	        });
	        state[action.id] = card;
	        return state;
	    }
	    if (action.type === 'LIST_POSTS_SUCCESS' && action.entity === 'card') {
	        state[action.card.entity_id] = action.card;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 12 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function chooseUnit() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'SET_CHOOSE_UNIT') {
	        return action.chooseUnit;
	    }
	    return state;
	};

/***/ },
/* 13 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function currentTreeUnit() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'SET_CURRENT_TREE_UNIT') {
	        return action.id;
	    }
	    return state;
	};

/***/ },
/* 14 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var cookie = __webpack_require__(8);

	module.exports = function currentUserID() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'SET_CURRENT_USER_ID') {
	        // TODO-2 I know this is horrible. This should be a listener.
	        if (action.currentUserID) {
	            cookie.set('currentUserID', action.currentUserID);
	        } else {
	            cookie.unset('currentUserID');
	        }
	        return action.currentUserID;
	    }
	    if (action.type === 'RESET_CURRENT_USER_ID') {
	        cookie.unset('currentUserID');
	        return '';
	    }
	    return state;
	};

/***/ },
/* 15 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

	/*

	{
	    kind
	    step (find, list, form, add, create)
	    selectedSubject
	        id
	        members
	    selectedUnit
	        id
	        members
	    subject
	    units
	    cards
	    searchResults /// use top level instead
	    myRecentSubjects
	    myRecentUnits
	    proposedUnit  // popped into units
	    proposedCard  // popped into cards
	}

	/create
	/create/subject/form  1
	/create/subject/add   1
	-> topic/proposal
	/create/unit/find 1
	/create/unit/list 2
	/create/unit/add  2
	/create/unit/create 2
	-> topic/proposal
	/create/card/find 1
	/create/card/list 2
	/create/card/create 2
	-> topic/proposal
	*/
	var _require = __webpack_require__(9),
	    shallowCopy = _require.shallowCopy,
	    copy = _require.copy;

	module.exports = function create() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'RESET_CREATE') {
	        return {};
	    }
	    if (action.type === 'UPDATE_CREATE_ROUTE') {
	        return Object.assign({}, state, {
	            kind: action.kind,
	            step: action.step
	        });
	    }
	    if (action.type === 'CREATE_SUBJECT_DATA') {
	        state = shallowCopy(state);
	        state.subject = action.values;
	        return state;
	    }
	    if (action.type === 'ADD_MEMBER_TO_CREATE_SUBJECT') {
	        state = shallowCopy(state);
	        state.subject = copy(state.subject || {});
	        var members = (state.subject.members || []).slice();
	        members.push({
	            kind: action.kind,
	            id: action.id,
	            name: action.name,
	            body: action.body
	        });
	        state.subject.members = members;
	        return state;
	    }
	    if (action.type === 'REMOVE_MEMBER_FROM_CREATE_SUBJECT') {
	        state = shallowCopy(state);
	        state.subject = copy(state.subject || {});
	        var _members = (state.subject.members || []).filter(function (member) {
	            return member.id !== action.id;
	        });
	        state.subject.members = _members;
	        return state;
	    }
	    if (action.type === 'REMOVE_UNIT_FROM_SUBJECT') {
	        state = shallowCopy(state);
	        var units = copy(state.units || []);
	        units.splice(action.index, 1);
	        state.units = units;
	        return state;
	    }
	    if (action.type === 'REMOVE_CARD_FROM_UNIT') {
	        state = shallowCopy(state);
	        var cards = copy(state.cards || []);
	        cards.splice(action.index, 1);
	        state.cards = cards;
	        return state;
	    }
	    if (action.type === 'SET_MY_RECENT_SUBJECTS') {
	        state = shallowCopy(state);
	        state.myRecentSubjects = action.subjects;
	        return state;
	    }
	    if (action.type === 'CREATE_CHOOSE_SUBJECT_FOR_UNITS') {
	        state = shallowCopy(state);
	        state.selectedSubject = {
	            id: action.id,
	            name: action.name
	        };
	        return state;
	    }
	    if (action.type === 'CREATE_CHOOSE_UNIT_FOR_CARDS') {
	        state = shallowCopy(state);
	        state.selectedUnit = {
	            id: action.id,
	            name: action.name
	        };
	        return state;
	    }
	    if (action.type === 'ADD_MEMBER_TO_ADD_UNITS') {
	        state = shallowCopy(state);
	        state.units = state.units && state.units.slice() || [];
	        state.units.push({
	            kind: action.kind,
	            id: action.id,
	            version: action.version,
	            name: action.name,
	            body: action.body,
	            require_ids: action.require_ids,
	            language: action.language
	        });
	        return state;
	    }
	    if (action.type === 'ADD_MEMBER_TO_ADD_CARDS') {
	        state = shallowCopy(state);
	        state.cards = state.cards && state.cards.slice() || [];
	        state.cards.push(action.values);
	        return state;
	    }
	    if (action.type === 'STOW_PROPOSED_UNIT') {
	        state = shallowCopy(state);
	        state.proposedUnit = copy(state.proposedUnit || {});
	        state.proposedUnit.name = action.name;
	        state.proposedUnit.language = action.language;
	        state.proposedUnit.body = action.body;
	        state.proposedUnit.require_ids = action.require_ids;
	        return state;
	    }
	    if (action.type === 'STOW_PROPOSED_CARD') {
	        state = shallowCopy(state);
	        state.proposedCard = action.values || {};
	        return state;
	    }
	    if (action.type === 'ADD_REQUIRE_TO_PROPOSED_UNIT') {
	        state = shallowCopy(state);
	        state.proposedUnit = copy(state.proposedUnit || {});
	        state.proposedUnit.require_ids = state.proposedUnit.require_ids || [];
	        state.proposedUnit.require_ids.push({
	            id: action.id,
	            name: action.name,
	            body: action.body,
	            kind: action.kind
	        });
	        return state;
	    }
	    if (action.type === 'ADD_LIST_FIELD_ROW' && state.proposedCard) {
	        state = shallowCopy(state);
	        var _action$values = action.values,
	            values = _action$values === undefined ? {} : _action$values;
	        var name = action.name,
	            columns = action.columns;

	        values = translateListOfRows(values, name);
	        values[name].push(columns.reduce(function (o, key) {
	            o[key] = '';
	            return o;
	        }, {}));
	        state.proposedCard = values;
	        return state;
	    }
	    if (action.type === 'REMOVE_LIST_FIELD_ROW' && state.proposedCard) {
	        state = shallowCopy(state);

	        var _action$values2 = action.values,
	            _values = _action$values2 === undefined ? {} : _action$values2;

	        var _name = action.name,
	            index = action.index;

	        _values = translateListOfRows(_values, _name);
	        _values[_name].splice(index, 1);
	        state.proposedCard = _values;
	        return state;
	    }
	    return state;
	};

	function translateListOfRows(values, name) {
	    values = copy(values);
	    Object.keys(values).forEach(function (key) {
	        if (key.indexOf(name) === 0) {
	            var _key$split = key.split('.'),
	                _key$split2 = _slicedToArray(_key$split, 3),
	                i = _key$split2[1],
	                field = _key$split2[2];

	            var index = parseInt(i, 10);
	            values[name] = values[name] || [];
	            values[name][index] = values[name][index] || {};
	            values[name][index][field] = values[key];
	            delete values[key];
	        }
	    });
	    return values;
	}

/***/ },
/* 16 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function errors() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'SET_ERRORS') {
	        return action.errors;
	    }
	    if (action.type === 'RESET_ERRORS') {
	        return [];
	    }
	    return state;
	};

/***/ },
/* 17 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(7),
	    mergeArraysByKey = _require.mergeArraysByKey;

	module.exports = function follows() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'LIST_FOLLOWS_SUCCESS') {
	        var _follows = mergeArraysByKey(state, action.follows, 'id');
	        return _follows;
	    }
	    if (action.type === 'ASK_FOLLOW_SUCCESS') {
	        if (action.follows.length === 0) {
	            return;
	        }
	        var follow = action.follows[0];
	        var _follows2 = state;
	        var index = _follows2.findIndex(function (f) {
	            return f.entity_id === action.entityID;
	        });
	        if (index > -1) {
	            _follows2[index] = follow;
	        } else {
	            _follows2.push(follow);
	        }
	        return _follows2;
	        // TODO-3 will this cause a bug with mergeArraysByKey later?
	    }
	    if (action.type === 'FOLLOW_SUCCESS') {
	        var _follows3 = state;
	        _follows3.push(action.follow);
	        return _follows3;
	        // TODO-3 will this cause a bug with mergeArraysByKey later?
	    }
	    if (action.type === 'UNFOLLOW_SUCCESS') {
	        var _follows4 = state;
	        var i = _follows4.findIndex(function (follow) {
	            return follow.id === action.id;
	        });
	        _follows4.splice(i, 1);
	        return _follows4;
	    }
	    return state;
	};

/***/ },
/* 18 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function formData() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'RESET_FORM_DATA') {
	        return {};
	    }
	    if (action.type === 'SET_FORM_DATA') {
	        return action.data;
	    }
	    return state;
	};

/***/ },
/* 19 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(9),
	    shallowCopy = _require.shallowCopy;

	module.exports = function learnCards() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_LEARN_CARD') {
	        state = shallowCopy(state);
	        state[action.id] = action.card;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 20 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var defaultState = { open: false, context: {} };

	var _require = __webpack_require__(9),
	    copy = _require.copy;

	module.exports = function menu() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : defaultState;
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'TOGGLE_MENU') {
	        var newState = copy(state);
	        newState.open = !state.open;
	        return newState;
	    }
	    if (action.type === 'UPDATE_MENU_CONTEXT') {
	        var _newState = copy(state);
	        if (action.card) {
	            _newState.context.card = action.card;
	        }
	        if (action.unit) {
	            _newState.context.unit = action.unit;
	        }
	        if (action.subject) {
	            _newState.context.subject = action.subject;
	        }
	        return _newState;
	    }
	    return state;
	};

/***/ },
/* 21 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function next() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'SET_NEXT') {
	        return action.next;
	    }
	    return state;
	};

/***/ },
/* 22 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(7),
	    mergeArraysByKey = _require.mergeArraysByKey;

	var _require2 = __webpack_require__(9),
	    copy = _require2.copy;

	module.exports = function notices() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'LIST_NOTICES_SUCCESS') {
	        var _notices = copy(state);
	        var newNotices = mergeArraysByKey(_notices, action.notices, 'id');
	        return newNotices;
	    }
	    if (action.type === 'MARK_NOTICE_SUCCESS') {
	        state.every(function (notice, index) {
	            if (notice.id === action.id) {
	                state[index] = action.notice;
	            }
	            return notice.id !== action.id;
	        });
	    }
	    return state;
	};

/***/ },
/* 23 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function passwordPageState() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'SET_PASSWORD_PAGE_STATE') {
	        return action.state;
	    }
	    return state;
	};

/***/ },
/* 24 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function recommendedSubjects() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'SET_RECOMMENDED_SUBJECTS') {
	        return action.recommendedSubjects;
	    }
	    return state;
	};

/***/ },
/* 25 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function route() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'SET_ROUTE') {
	        return action.route;
	    }
	    return state;
	};

/***/ },
/* 26 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function routeQuery() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'SET_ROUTE') {
	        return action.routeQuery;
	    }
	    return state;
	};

/***/ },
/* 27 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function routeQuery() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'SET_ROUTE') {
	        return action.title;
	    }
	    return state;
	};

/***/ },
/* 28 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function searchQuery() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'RESET_SEARCH') {
	        return '';
	    }
	    if (action.type === 'SET_SEARCH_QUERY') {
	        return action.q;
	    }
	    return state;
	};

/***/ },
/* 29 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(7),
	    mergeArraysByKey = _require.mergeArraysByKey;

	module.exports = function searchResults() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'RESET_SEARCH') {
	        return [];
	    }
	    if (action.type === 'ADD_SEARCH_RESULTS') {
	        return mergeArraysByKey(state, action.results, 'id');
	    }
	    return state;
	};

/***/ },
/* 30 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function sending() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : false;
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'SET_SENDING_ON') {
	        return true;
	    }
	    if (action.type === 'SET_SENDING_OFF') {
	        return false;
	    }
	    return state;
	};

/***/ },
/* 31 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(9),
	    shallowCopy = _require.shallowCopy;

	module.exports = function subjectTree() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_SUBJECT_TREE') {
	        state = shallowCopy(state);
	        state[action.id] = action.tree;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 32 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(7),
	    mergeArraysByKey = _require.mergeArraysByKey;

	var _require2 = __webpack_require__(9),
	    shallowCopy = _require2.shallowCopy;

	module.exports = function subjectVersions() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_SUBJECT_VERSIONS') {
	        var versions = state[action.entity_id] || [];
	        versions = mergeArraysByKey(versions, action.versions, 'id' // id is the version id
	        );
	        state = shallowCopy(state);
	        state[action.entity_id] = versions;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 33 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(9),
	    shallowCopy = _require.shallowCopy;

	module.exports = function subjects() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_SUBJECT') {
	        state = shallowCopy(state);
	        state[action.subject.entity_id] = action.subject;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 34 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(9),
	    shallowCopy = _require.shallowCopy;

	var _require2 = __webpack_require__(7),
	    mergeArraysByKey = _require2.mergeArraysByKey;

	module.exports = function topicPosts() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_TOPIC_POSTS') {
	        state = shallowCopy(state);
	        var posts = state[action.topic_id] || [];
	        posts = mergeArraysByKey(posts, action.posts, 'id');
	        state[action.topic_id] = posts;
	        return state;
	    }
	    if (action.type === 'UPDATE_POST_SUCCESS') {
	        state = shallowCopy(state);
	        var _posts = state[action.topicId].slice() || [];
	        var index = _posts.findIndex(function (post) {
	            return post.id === action.postId;
	        });
	        _posts[index] = action.post;
	        state[action.topicId] = _posts;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 35 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(9),
	    shallowCopy = _require.shallowCopy;

	module.exports = function topicPostVersions() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {
	        card: {},
	        unit: {},
	        subject: {}
	    };
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_TOPIC_POST_VERSIONS_CARD') {
	        state.card = shallowCopy(state.card);
	        state.card[action.version.id] = action.version;
	        return state;
	    }
	    if (action.type === 'ADD_TOPIC_POST_VERSIONS_UNIT') {
	        state.unit = shallowCopy(state.unit);
	        state.unit[action.version.id] = action.version;
	        return state;
	    }
	    if (action.type === 'ADD_TOPIC_POST_VERSIONS_SUBJECT') {
	        state.subject = shallowCopy(state.subject);
	        state.subject[action.version.id] = action.version;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 36 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(9),
	    shallowCopy = _require.shallowCopy;

	module.exports = function topics() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_TOPIC') {
	        state = shallowCopy(state);
	        state[action.id || action.topic.id] = action.topic;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 37 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(9),
	    shallowCopy = _require.shallowCopy;

	module.exports = function unitLearned() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_UNIT_LEARNED') {
	        state = shallowCopy(state);
	        state[action.unit_id] = action.learned;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 38 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(7),
	    mergeArraysByKey = _require.mergeArraysByKey;

	var _require2 = __webpack_require__(9),
	    shallowCopy = _require2.shallowCopy;

	module.exports = function unitVersions() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_UNIT_VERSIONS') {
	        var versions = state[action.entity_id] || [];
	        versions = mergeArraysByKey(versions, action.versions, 'id' // id is the version id
	        );
	        state = shallowCopy(state);
	        state[action.entity_id] = versions;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 39 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(9),
	    shallowCopy = _require.shallowCopy;

	module.exports = function units() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_UNIT') {
	        state = shallowCopy(state);
	        state[action.unit.entity_id] = action.unit;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 40 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(9),
	    shallowCopy = _require.shallowCopy;

	module.exports = function users() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_USER') {
	        state = shallowCopy(state);
	        state[action.user.id] = action.user;
	        return state;
	    }
	    return state;
	};

/***/ },
/* 41 */
/***/ function(module, exports) {

	'use strict';

	module.exports = function userAvatars() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_USER_AVATARS') {
	        return Object.assign({}, state, action.avatars);
	    }
	    return state;
	};

/***/ },
/* 42 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(7),
	    mergeArraysByKey = _require.mergeArraysByKey;

	module.exports = function userSubjects() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
	    var action = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : { type: '' };

	    if (action.type === 'ADD_USER_SUBJECTS') {
	        return mergeArraysByKey(state, action.subjects, 'id');
	    }
	    return state;
	};

/***/ },
/* 43 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable prefer-arrow-callback */
	var diff = __webpack_require__(44);
	var patch = __webpack_require__(57);
	var createElement = __webpack_require__(66);
	var virtualize = __webpack_require__(67);

	var store = __webpack_require__(2);

	var _require = __webpack_require__(2),
	    getState = _require.getState;

	var broker = __webpack_require__(71);

	module.exports = function init(options) {
	    var view = options.view,
	        el = options.el;


	    var tree = void 0;
	    var root = void 0;

	    if (el.innerHTML.trim()) {
	        tree = virtualize(el);
	        root = el.children[0];
	    } else {
	        tree = view(getState());
	        root = createElement(tree);
	        el.innerHTML = '';
	        el.appendChild(root);
	    }

	    store.bind(function update(data) {
	        var next = view(data);
	        root = patch(root, diff(tree, next));
	        tree = next;
	    });

	    broker.observe(el);
	};

/***/ },
/* 44 */
/***/ function(module, exports, __webpack_require__) {

	var diff = __webpack_require__(45)

	module.exports = diff


/***/ },
/* 45 */
/***/ function(module, exports, __webpack_require__) {

	var isArray = __webpack_require__(46)

	var VPatch = __webpack_require__(47)
	var isVNode = __webpack_require__(49)
	var isVText = __webpack_require__(50)
	var isWidget = __webpack_require__(51)
	var isThunk = __webpack_require__(52)
	var handleThunk = __webpack_require__(53)

	var diffProps = __webpack_require__(54)

	module.exports = diff

	function diff(a, b) {
	    var patch = { a: a }
	    walk(a, b, patch, 0)
	    return patch
	}

	function walk(a, b, patch, index) {
	    if (a === b) {
	        return
	    }

	    var apply = patch[index]
	    var applyClear = false

	    if (isThunk(a) || isThunk(b)) {
	        thunks(a, b, patch, index)
	    } else if (b == null) {

	        // If a is a widget we will add a remove patch for it
	        // Otherwise any child widgets/hooks must be destroyed.
	        // This prevents adding two remove patches for a widget.
	        if (!isWidget(a)) {
	            clearState(a, patch, index)
	            apply = patch[index]
	        }

	        apply = appendPatch(apply, new VPatch(VPatch.REMOVE, a, b))
	    } else if (isVNode(b)) {
	        if (isVNode(a)) {
	            if (a.tagName === b.tagName &&
	                a.namespace === b.namespace &&
	                a.key === b.key) {
	                var propsPatch = diffProps(a.properties, b.properties)
	                if (propsPatch) {
	                    apply = appendPatch(apply,
	                        new VPatch(VPatch.PROPS, a, propsPatch))
	                }
	                apply = diffChildren(a, b, patch, apply, index)
	            } else {
	                apply = appendPatch(apply, new VPatch(VPatch.VNODE, a, b))
	                applyClear = true
	            }
	        } else {
	            apply = appendPatch(apply, new VPatch(VPatch.VNODE, a, b))
	            applyClear = true
	        }
	    } else if (isVText(b)) {
	        if (!isVText(a)) {
	            apply = appendPatch(apply, new VPatch(VPatch.VTEXT, a, b))
	            applyClear = true
	        } else if (a.text !== b.text) {
	            apply = appendPatch(apply, new VPatch(VPatch.VTEXT, a, b))
	        }
	    } else if (isWidget(b)) {
	        if (!isWidget(a)) {
	            applyClear = true
	        }

	        apply = appendPatch(apply, new VPatch(VPatch.WIDGET, a, b))
	    }

	    if (apply) {
	        patch[index] = apply
	    }

	    if (applyClear) {
	        clearState(a, patch, index)
	    }
	}

	function diffChildren(a, b, patch, apply, index) {
	    var aChildren = a.children
	    var orderedSet = reorder(aChildren, b.children)
	    var bChildren = orderedSet.children

	    var aLen = aChildren.length
	    var bLen = bChildren.length
	    var len = aLen > bLen ? aLen : bLen

	    for (var i = 0; i < len; i++) {
	        var leftNode = aChildren[i]
	        var rightNode = bChildren[i]
	        index += 1

	        if (!leftNode) {
	            if (rightNode) {
	                // Excess nodes in b need to be added
	                apply = appendPatch(apply,
	                    new VPatch(VPatch.INSERT, null, rightNode))
	            }
	        } else {
	            walk(leftNode, rightNode, patch, index)
	        }

	        if (isVNode(leftNode) && leftNode.count) {
	            index += leftNode.count
	        }
	    }

	    if (orderedSet.moves) {
	        // Reorder nodes last
	        apply = appendPatch(apply, new VPatch(
	            VPatch.ORDER,
	            a,
	            orderedSet.moves
	        ))
	    }

	    return apply
	}

	function clearState(vNode, patch, index) {
	    // TODO: Make this a single walk, not two
	    unhook(vNode, patch, index)
	    destroyWidgets(vNode, patch, index)
	}

	// Patch records for all destroyed widgets must be added because we need
	// a DOM node reference for the destroy function
	function destroyWidgets(vNode, patch, index) {
	    if (isWidget(vNode)) {
	        if (typeof vNode.destroy === "function") {
	            patch[index] = appendPatch(
	                patch[index],
	                new VPatch(VPatch.REMOVE, vNode, null)
	            )
	        }
	    } else if (isVNode(vNode) && (vNode.hasWidgets || vNode.hasThunks)) {
	        var children = vNode.children
	        var len = children.length
	        for (var i = 0; i < len; i++) {
	            var child = children[i]
	            index += 1

	            destroyWidgets(child, patch, index)

	            if (isVNode(child) && child.count) {
	                index += child.count
	            }
	        }
	    } else if (isThunk(vNode)) {
	        thunks(vNode, null, patch, index)
	    }
	}

	// Create a sub-patch for thunks
	function thunks(a, b, patch, index) {
	    var nodes = handleThunk(a, b)
	    var thunkPatch = diff(nodes.a, nodes.b)
	    if (hasPatches(thunkPatch)) {
	        patch[index] = new VPatch(VPatch.THUNK, null, thunkPatch)
	    }
	}

	function hasPatches(patch) {
	    for (var index in patch) {
	        if (index !== "a") {
	            return true
	        }
	    }

	    return false
	}

	// Execute hooks when two nodes are identical
	function unhook(vNode, patch, index) {
	    if (isVNode(vNode)) {
	        if (vNode.hooks) {
	            patch[index] = appendPatch(
	                patch[index],
	                new VPatch(
	                    VPatch.PROPS,
	                    vNode,
	                    undefinedKeys(vNode.hooks)
	                )
	            )
	        }

	        if (vNode.descendantHooks || vNode.hasThunks) {
	            var children = vNode.children
	            var len = children.length
	            for (var i = 0; i < len; i++) {
	                var child = children[i]
	                index += 1

	                unhook(child, patch, index)

	                if (isVNode(child) && child.count) {
	                    index += child.count
	                }
	            }
	        }
	    } else if (isThunk(vNode)) {
	        thunks(vNode, null, patch, index)
	    }
	}

	function undefinedKeys(obj) {
	    var result = {}

	    for (var key in obj) {
	        result[key] = undefined
	    }

	    return result
	}

	// List diff, naive left to right reordering
	function reorder(aChildren, bChildren) {
	    // O(M) time, O(M) memory
	    var bChildIndex = keyIndex(bChildren)
	    var bKeys = bChildIndex.keys
	    var bFree = bChildIndex.free

	    if (bFree.length === bChildren.length) {
	        return {
	            children: bChildren,
	            moves: null
	        }
	    }

	    // O(N) time, O(N) memory
	    var aChildIndex = keyIndex(aChildren)
	    var aKeys = aChildIndex.keys
	    var aFree = aChildIndex.free

	    if (aFree.length === aChildren.length) {
	        return {
	            children: bChildren,
	            moves: null
	        }
	    }

	    // O(MAX(N, M)) memory
	    var newChildren = []

	    var freeIndex = 0
	    var freeCount = bFree.length
	    var deletedItems = 0

	    // Iterate through a and match a node in b
	    // O(N) time,
	    for (var i = 0 ; i < aChildren.length; i++) {
	        var aItem = aChildren[i]
	        var itemIndex

	        if (aItem.key) {
	            if (bKeys.hasOwnProperty(aItem.key)) {
	                // Match up the old keys
	                itemIndex = bKeys[aItem.key]
	                newChildren.push(bChildren[itemIndex])

	            } else {
	                // Remove old keyed items
	                itemIndex = i - deletedItems++
	                newChildren.push(null)
	            }
	        } else {
	            // Match the item in a with the next free item in b
	            if (freeIndex < freeCount) {
	                itemIndex = bFree[freeIndex++]
	                newChildren.push(bChildren[itemIndex])
	            } else {
	                // There are no free items in b to match with
	                // the free items in a, so the extra free nodes
	                // are deleted.
	                itemIndex = i - deletedItems++
	                newChildren.push(null)
	            }
	        }
	    }

	    var lastFreeIndex = freeIndex >= bFree.length ?
	        bChildren.length :
	        bFree[freeIndex]

	    // Iterate through b and append any new keys
	    // O(M) time
	    for (var j = 0; j < bChildren.length; j++) {
	        var newItem = bChildren[j]

	        if (newItem.key) {
	            if (!aKeys.hasOwnProperty(newItem.key)) {
	                // Add any new keyed items
	                // We are adding new items to the end and then sorting them
	                // in place. In future we should insert new items in place.
	                newChildren.push(newItem)
	            }
	        } else if (j >= lastFreeIndex) {
	            // Add any leftover non-keyed items
	            newChildren.push(newItem)
	        }
	    }

	    var simulate = newChildren.slice()
	    var simulateIndex = 0
	    var removes = []
	    var inserts = []
	    var simulateItem

	    for (var k = 0; k < bChildren.length;) {
	        var wantedItem = bChildren[k]
	        simulateItem = simulate[simulateIndex]

	        // remove items
	        while (simulateItem === null && simulate.length) {
	            removes.push(remove(simulate, simulateIndex, null))
	            simulateItem = simulate[simulateIndex]
	        }

	        if (!simulateItem || simulateItem.key !== wantedItem.key) {
	            // if we need a key in this position...
	            if (wantedItem.key) {
	                if (simulateItem && simulateItem.key) {
	                    // if an insert doesn't put this key in place, it needs to move
	                    if (bKeys[simulateItem.key] !== k + 1) {
	                        removes.push(remove(simulate, simulateIndex, simulateItem.key))
	                        simulateItem = simulate[simulateIndex]
	                        // if the remove didn't put the wanted item in place, we need to insert it
	                        if (!simulateItem || simulateItem.key !== wantedItem.key) {
	                            inserts.push({key: wantedItem.key, to: k})
	                        }
	                        // items are matching, so skip ahead
	                        else {
	                            simulateIndex++
	                        }
	                    }
	                    else {
	                        inserts.push({key: wantedItem.key, to: k})
	                    }
	                }
	                else {
	                    inserts.push({key: wantedItem.key, to: k})
	                }
	                k++
	            }
	            // a key in simulate has no matching wanted key, remove it
	            else if (simulateItem && simulateItem.key) {
	                removes.push(remove(simulate, simulateIndex, simulateItem.key))
	            }
	        }
	        else {
	            simulateIndex++
	            k++
	        }
	    }

	    // remove all the remaining nodes from simulate
	    while(simulateIndex < simulate.length) {
	        simulateItem = simulate[simulateIndex]
	        removes.push(remove(simulate, simulateIndex, simulateItem && simulateItem.key))
	    }

	    // If the only moves we have are deletes then we can just
	    // let the delete patch remove these items.
	    if (removes.length === deletedItems && !inserts.length) {
	        return {
	            children: newChildren,
	            moves: null
	        }
	    }

	    return {
	        children: newChildren,
	        moves: {
	            removes: removes,
	            inserts: inserts
	        }
	    }
	}

	function remove(arr, index, key) {
	    arr.splice(index, 1)

	    return {
	        from: index,
	        key: key
	    }
	}

	function keyIndex(children) {
	    var keys = {}
	    var free = []
	    var length = children.length

	    for (var i = 0; i < length; i++) {
	        var child = children[i]

	        if (child.key) {
	            keys[child.key] = i
	        } else {
	            free.push(i)
	        }
	    }

	    return {
	        keys: keys,     // A hash of key name to index
	        free: free      // An array of unkeyed item indices
	    }
	}

	function appendPatch(apply, patch) {
	    if (apply) {
	        if (isArray(apply)) {
	            apply.push(patch)
	        } else {
	            apply = [apply, patch]
	        }

	        return apply
	    } else {
	        return patch
	    }
	}


/***/ },
/* 46 */
/***/ function(module, exports) {

	var nativeIsArray = Array.isArray
	var toString = Object.prototype.toString

	module.exports = nativeIsArray || isArray

	function isArray(obj) {
	    return toString.call(obj) === "[object Array]"
	}


/***/ },
/* 47 */
/***/ function(module, exports, __webpack_require__) {

	var version = __webpack_require__(48)

	VirtualPatch.NONE = 0
	VirtualPatch.VTEXT = 1
	VirtualPatch.VNODE = 2
	VirtualPatch.WIDGET = 3
	VirtualPatch.PROPS = 4
	VirtualPatch.ORDER = 5
	VirtualPatch.INSERT = 6
	VirtualPatch.REMOVE = 7
	VirtualPatch.THUNK = 8

	module.exports = VirtualPatch

	function VirtualPatch(type, vNode, patch) {
	    this.type = Number(type)
	    this.vNode = vNode
	    this.patch = patch
	}

	VirtualPatch.prototype.version = version
	VirtualPatch.prototype.type = "VirtualPatch"


/***/ },
/* 48 */
/***/ function(module, exports) {

	module.exports = "2"


/***/ },
/* 49 */
/***/ function(module, exports, __webpack_require__) {

	var version = __webpack_require__(48)

	module.exports = isVirtualNode

	function isVirtualNode(x) {
	    return x && x.type === "VirtualNode" && x.version === version
	}


/***/ },
/* 50 */
/***/ function(module, exports, __webpack_require__) {

	var version = __webpack_require__(48)

	module.exports = isVirtualText

	function isVirtualText(x) {
	    return x && x.type === "VirtualText" && x.version === version
	}


/***/ },
/* 51 */
/***/ function(module, exports) {

	module.exports = isWidget

	function isWidget(w) {
	    return w && w.type === "Widget"
	}


/***/ },
/* 52 */
/***/ function(module, exports) {

	module.exports = isThunk

	function isThunk(t) {
	    return t && t.type === "Thunk"
	}


/***/ },
/* 53 */
/***/ function(module, exports, __webpack_require__) {

	var isVNode = __webpack_require__(49)
	var isVText = __webpack_require__(50)
	var isWidget = __webpack_require__(51)
	var isThunk = __webpack_require__(52)

	module.exports = handleThunk

	function handleThunk(a, b) {
	    var renderedA = a
	    var renderedB = b

	    if (isThunk(b)) {
	        renderedB = renderThunk(b, a)
	    }

	    if (isThunk(a)) {
	        renderedA = renderThunk(a, null)
	    }

	    return {
	        a: renderedA,
	        b: renderedB
	    }
	}

	function renderThunk(thunk, previous) {
	    var renderedThunk = thunk.vnode

	    if (!renderedThunk) {
	        renderedThunk = thunk.vnode = thunk.render(previous)
	    }

	    if (!(isVNode(renderedThunk) ||
	            isVText(renderedThunk) ||
	            isWidget(renderedThunk))) {
	        throw new Error("thunk did not return a valid node");
	    }

	    return renderedThunk
	}


/***/ },
/* 54 */
/***/ function(module, exports, __webpack_require__) {

	var isObject = __webpack_require__(55)
	var isHook = __webpack_require__(56)

	module.exports = diffProps

	function diffProps(a, b) {
	    var diff

	    for (var aKey in a) {
	        if (!(aKey in b)) {
	            diff = diff || {}
	            diff[aKey] = undefined
	        }

	        var aValue = a[aKey]
	        var bValue = b[aKey]

	        if (aValue === bValue) {
	            continue
	        } else if (isObject(aValue) && isObject(bValue)) {
	            if (getPrototype(bValue) !== getPrototype(aValue)) {
	                diff = diff || {}
	                diff[aKey] = bValue
	            } else if (isHook(bValue)) {
	                 diff = diff || {}
	                 diff[aKey] = bValue
	            } else {
	                var objectDiff = diffProps(aValue, bValue)
	                if (objectDiff) {
	                    diff = diff || {}
	                    diff[aKey] = objectDiff
	                }
	            }
	        } else {
	            diff = diff || {}
	            diff[aKey] = bValue
	        }
	    }

	    for (var bKey in b) {
	        if (!(bKey in a)) {
	            diff = diff || {}
	            diff[bKey] = b[bKey]
	        }
	    }

	    return diff
	}

	function getPrototype(value) {
	  if (Object.getPrototypeOf) {
	    return Object.getPrototypeOf(value)
	  } else if (value.__proto__) {
	    return value.__proto__
	  } else if (value.constructor) {
	    return value.constructor.prototype
	  }
	}


/***/ },
/* 55 */
/***/ function(module, exports) {

	"use strict";

	module.exports = function isObject(x) {
		return typeof x === "object" && x !== null;
	};


/***/ },
/* 56 */
/***/ function(module, exports) {

	module.exports = isHook

	function isHook(hook) {
	    return hook &&
	      (typeof hook.hook === "function" && !hook.hasOwnProperty("hook") ||
	       typeof hook.unhook === "function" && !hook.hasOwnProperty("unhook"))
	}


/***/ },
/* 57 */
/***/ function(module, exports, __webpack_require__) {

	var patch = __webpack_require__(58)

	module.exports = patch


/***/ },
/* 58 */
/***/ function(module, exports, __webpack_require__) {

	var document = __webpack_require__(59)
	var isArray = __webpack_require__(46)

	var render = __webpack_require__(61)
	var domIndex = __webpack_require__(63)
	var patchOp = __webpack_require__(64)
	module.exports = patch

	function patch(rootNode, patches, renderOptions) {
	    renderOptions = renderOptions || {}
	    renderOptions.patch = renderOptions.patch && renderOptions.patch !== patch
	        ? renderOptions.patch
	        : patchRecursive
	    renderOptions.render = renderOptions.render || render

	    return renderOptions.patch(rootNode, patches, renderOptions)
	}

	function patchRecursive(rootNode, patches, renderOptions) {
	    var indices = patchIndices(patches)

	    if (indices.length === 0) {
	        return rootNode
	    }

	    var index = domIndex(rootNode, patches.a, indices)
	    var ownerDocument = rootNode.ownerDocument

	    if (!renderOptions.document && ownerDocument !== document) {
	        renderOptions.document = ownerDocument
	    }

	    for (var i = 0; i < indices.length; i++) {
	        var nodeIndex = indices[i]
	        rootNode = applyPatch(rootNode,
	            index[nodeIndex],
	            patches[nodeIndex],
	            renderOptions)
	    }

	    return rootNode
	}

	function applyPatch(rootNode, domNode, patchList, renderOptions) {
	    if (!domNode) {
	        return rootNode
	    }

	    var newNode

	    if (isArray(patchList)) {
	        for (var i = 0; i < patchList.length; i++) {
	            newNode = patchOp(patchList[i], domNode, renderOptions)

	            if (domNode === rootNode) {
	                rootNode = newNode
	            }
	        }
	    } else {
	        newNode = patchOp(patchList, domNode, renderOptions)

	        if (domNode === rootNode) {
	            rootNode = newNode
	        }
	    }

	    return rootNode
	}

	function patchIndices(patches) {
	    var indices = []

	    for (var key in patches) {
	        if (key !== "a") {
	            indices.push(Number(key))
	        }
	    }

	    return indices
	}


/***/ },
/* 59 */
/***/ function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(global) {var topLevel = typeof global !== 'undefined' ? global :
	    typeof window !== 'undefined' ? window : {}
	var minDoc = __webpack_require__(60);

	var doccy;

	if (typeof document !== 'undefined') {
	    doccy = document;
	} else {
	    doccy = topLevel['__GLOBAL_DOCUMENT_CACHE@4'];

	    if (!doccy) {
	        doccy = topLevel['__GLOBAL_DOCUMENT_CACHE@4'] = minDoc;
	    }
	}

	module.exports = doccy;

	/* WEBPACK VAR INJECTION */}.call(exports, (function() { return this; }())))

/***/ },
/* 60 */
/***/ function(module, exports) {

	/* (ignored) */

/***/ },
/* 61 */
/***/ function(module, exports, __webpack_require__) {

	var document = __webpack_require__(59)

	var applyProperties = __webpack_require__(62)

	var isVNode = __webpack_require__(49)
	var isVText = __webpack_require__(50)
	var isWidget = __webpack_require__(51)
	var handleThunk = __webpack_require__(53)

	module.exports = createElement

	function createElement(vnode, opts) {
	    var doc = opts ? opts.document || document : document
	    var warn = opts ? opts.warn : null

	    vnode = handleThunk(vnode).a

	    if (isWidget(vnode)) {
	        return vnode.init()
	    } else if (isVText(vnode)) {
	        return doc.createTextNode(vnode.text)
	    } else if (!isVNode(vnode)) {
	        if (warn) {
	            warn("Item is not a valid virtual dom node", vnode)
	        }
	        return null
	    }

	    var node = (vnode.namespace === null) ?
	        doc.createElement(vnode.tagName) :
	        doc.createElementNS(vnode.namespace, vnode.tagName)

	    var props = vnode.properties
	    applyProperties(node, props)

	    var children = vnode.children

	    for (var i = 0; i < children.length; i++) {
	        var childNode = createElement(children[i], opts)
	        if (childNode) {
	            node.appendChild(childNode)
	        }
	    }

	    return node
	}


/***/ },
/* 62 */
/***/ function(module, exports, __webpack_require__) {

	var isObject = __webpack_require__(55)
	var isHook = __webpack_require__(56)

	module.exports = applyProperties

	function applyProperties(node, props, previous) {
	    for (var propName in props) {
	        var propValue = props[propName]

	        if (propValue === undefined) {
	            removeProperty(node, propName, propValue, previous);
	        } else if (isHook(propValue)) {
	            removeProperty(node, propName, propValue, previous)
	            if (propValue.hook) {
	                propValue.hook(node,
	                    propName,
	                    previous ? previous[propName] : undefined)
	            }
	        } else {
	            if (isObject(propValue)) {
	                patchObject(node, props, previous, propName, propValue);
	            } else {
	                node[propName] = propValue
	            }
	        }
	    }
	}

	function removeProperty(node, propName, propValue, previous) {
	    if (previous) {
	        var previousValue = previous[propName]

	        if (!isHook(previousValue)) {
	            if (propName === "attributes") {
	                for (var attrName in previousValue) {
	                    node.removeAttribute(attrName)
	                }
	            } else if (propName === "style") {
	                for (var i in previousValue) {
	                    node.style[i] = ""
	                }
	            } else if (typeof previousValue === "string") {
	                node[propName] = ""
	            } else {
	                node[propName] = null
	            }
	        } else if (previousValue.unhook) {
	            previousValue.unhook(node, propName, propValue)
	        }
	    }
	}

	function patchObject(node, props, previous, propName, propValue) {
	    var previousValue = previous ? previous[propName] : undefined

	    // Set attributes
	    if (propName === "attributes") {
	        for (var attrName in propValue) {
	            var attrValue = propValue[attrName]

	            if (attrValue === undefined) {
	                node.removeAttribute(attrName)
	            } else {
	                node.setAttribute(attrName, attrValue)
	            }
	        }

	        return
	    }

	    if(previousValue && isObject(previousValue) &&
	        getPrototype(previousValue) !== getPrototype(propValue)) {
	        node[propName] = propValue
	        return
	    }

	    if (!isObject(node[propName])) {
	        node[propName] = {}
	    }

	    var replacer = propName === "style" ? "" : undefined

	    for (var k in propValue) {
	        var value = propValue[k]
	        node[propName][k] = (value === undefined) ? replacer : value
	    }
	}

	function getPrototype(value) {
	    if (Object.getPrototypeOf) {
	        return Object.getPrototypeOf(value)
	    } else if (value.__proto__) {
	        return value.__proto__
	    } else if (value.constructor) {
	        return value.constructor.prototype
	    }
	}


/***/ },
/* 63 */
/***/ function(module, exports) {

	// Maps a virtual DOM tree onto a real DOM tree in an efficient manner.
	// We don't want to read all of the DOM nodes in the tree so we use
	// the in-order tree indexing to eliminate recursion down certain branches.
	// We only recurse into a DOM node if we know that it contains a child of
	// interest.

	var noChild = {}

	module.exports = domIndex

	function domIndex(rootNode, tree, indices, nodes) {
	    if (!indices || indices.length === 0) {
	        return {}
	    } else {
	        indices.sort(ascending)
	        return recurse(rootNode, tree, indices, nodes, 0)
	    }
	}

	function recurse(rootNode, tree, indices, nodes, rootIndex) {
	    nodes = nodes || {}


	    if (rootNode) {
	        if (indexInRange(indices, rootIndex, rootIndex)) {
	            nodes[rootIndex] = rootNode
	        }

	        var vChildren = tree.children

	        if (vChildren) {

	            var childNodes = rootNode.childNodes

	            for (var i = 0; i < tree.children.length; i++) {
	                rootIndex += 1

	                var vChild = vChildren[i] || noChild
	                var nextIndex = rootIndex + (vChild.count || 0)

	                // skip recursion down the tree if there are no nodes down here
	                if (indexInRange(indices, rootIndex, nextIndex)) {
	                    recurse(childNodes[i], vChild, indices, nodes, rootIndex)
	                }

	                rootIndex = nextIndex
	            }
	        }
	    }

	    return nodes
	}

	// Binary search for an index in the interval [left, right]
	function indexInRange(indices, left, right) {
	    if (indices.length === 0) {
	        return false
	    }

	    var minIndex = 0
	    var maxIndex = indices.length - 1
	    var currentIndex
	    var currentItem

	    while (minIndex <= maxIndex) {
	        currentIndex = ((maxIndex + minIndex) / 2) >> 0
	        currentItem = indices[currentIndex]

	        if (minIndex === maxIndex) {
	            return currentItem >= left && currentItem <= right
	        } else if (currentItem < left) {
	            minIndex = currentIndex + 1
	        } else  if (currentItem > right) {
	            maxIndex = currentIndex - 1
	        } else {
	            return true
	        }
	    }

	    return false;
	}

	function ascending(a, b) {
	    return a > b ? 1 : -1
	}


/***/ },
/* 64 */
/***/ function(module, exports, __webpack_require__) {

	var applyProperties = __webpack_require__(62)

	var isWidget = __webpack_require__(51)
	var VPatch = __webpack_require__(47)

	var updateWidget = __webpack_require__(65)

	module.exports = applyPatch

	function applyPatch(vpatch, domNode, renderOptions) {
	    var type = vpatch.type
	    var vNode = vpatch.vNode
	    var patch = vpatch.patch

	    switch (type) {
	        case VPatch.REMOVE:
	            return removeNode(domNode, vNode)
	        case VPatch.INSERT:
	            return insertNode(domNode, patch, renderOptions)
	        case VPatch.VTEXT:
	            return stringPatch(domNode, vNode, patch, renderOptions)
	        case VPatch.WIDGET:
	            return widgetPatch(domNode, vNode, patch, renderOptions)
	        case VPatch.VNODE:
	            return vNodePatch(domNode, vNode, patch, renderOptions)
	        case VPatch.ORDER:
	            reorderChildren(domNode, patch)
	            return domNode
	        case VPatch.PROPS:
	            applyProperties(domNode, patch, vNode.properties)
	            return domNode
	        case VPatch.THUNK:
	            return replaceRoot(domNode,
	                renderOptions.patch(domNode, patch, renderOptions))
	        default:
	            return domNode
	    }
	}

	function removeNode(domNode, vNode) {
	    var parentNode = domNode.parentNode

	    if (parentNode) {
	        parentNode.removeChild(domNode)
	    }

	    destroyWidget(domNode, vNode);

	    return null
	}

	function insertNode(parentNode, vNode, renderOptions) {
	    var newNode = renderOptions.render(vNode, renderOptions)

	    if (parentNode) {
	        parentNode.appendChild(newNode)
	    }

	    return parentNode
	}

	function stringPatch(domNode, leftVNode, vText, renderOptions) {
	    var newNode

	    if (domNode.nodeType === 3) {
	        domNode.replaceData(0, domNode.length, vText.text)
	        newNode = domNode
	    } else {
	        var parentNode = domNode.parentNode
	        newNode = renderOptions.render(vText, renderOptions)

	        if (parentNode && newNode !== domNode) {
	            parentNode.replaceChild(newNode, domNode)
	        }
	    }

	    return newNode
	}

	function widgetPatch(domNode, leftVNode, widget, renderOptions) {
	    var updating = updateWidget(leftVNode, widget)
	    var newNode

	    if (updating) {
	        newNode = widget.update(leftVNode, domNode) || domNode
	    } else {
	        newNode = renderOptions.render(widget, renderOptions)
	    }

	    var parentNode = domNode.parentNode

	    if (parentNode && newNode !== domNode) {
	        parentNode.replaceChild(newNode, domNode)
	    }

	    if (!updating) {
	        destroyWidget(domNode, leftVNode)
	    }

	    return newNode
	}

	function vNodePatch(domNode, leftVNode, vNode, renderOptions) {
	    var parentNode = domNode.parentNode
	    var newNode = renderOptions.render(vNode, renderOptions)

	    if (parentNode && newNode !== domNode) {
	        parentNode.replaceChild(newNode, domNode)
	    }

	    return newNode
	}

	function destroyWidget(domNode, w) {
	    if (typeof w.destroy === "function" && isWidget(w)) {
	        w.destroy(domNode)
	    }
	}

	function reorderChildren(domNode, moves) {
	    var childNodes = domNode.childNodes
	    var keyMap = {}
	    var node
	    var remove
	    var insert

	    for (var i = 0; i < moves.removes.length; i++) {
	        remove = moves.removes[i]
	        node = childNodes[remove.from]
	        if (remove.key) {
	            keyMap[remove.key] = node
	        }
	        domNode.removeChild(node)
	    }

	    var length = childNodes.length
	    for (var j = 0; j < moves.inserts.length; j++) {
	        insert = moves.inserts[j]
	        node = keyMap[insert.key]
	        // this is the weirdest bug i've ever seen in webkit
	        domNode.insertBefore(node, insert.to >= length++ ? null : childNodes[insert.to])
	    }
	}

	function replaceRoot(oldRoot, newRoot) {
	    if (oldRoot && newRoot && oldRoot !== newRoot && oldRoot.parentNode) {
	        oldRoot.parentNode.replaceChild(newRoot, oldRoot)
	    }

	    return newRoot;
	}


/***/ },
/* 65 */
/***/ function(module, exports, __webpack_require__) {

	var isWidget = __webpack_require__(51)

	module.exports = updateWidget

	function updateWidget(a, b) {
	    if (isWidget(a) && isWidget(b)) {
	        if ("name" in a && "name" in b) {
	            return a.id === b.id
	        } else {
	            return a.init === b.init
	        }
	    }

	    return false
	}


/***/ },
/* 66 */
/***/ function(module, exports, __webpack_require__) {

	var createElement = __webpack_require__(61)

	module.exports = createElement


/***/ },
/* 67 */
/***/ function(module, exports, __webpack_require__) {

	/*!
	* vdom-virtualize
	* Copyright 2014 by Marcel Klehr <mklehr@gmx.net>
	*
	* (MIT LICENSE)
	* Permission is hereby granted, free of charge, to any person obtaining a copy
	* of this software and associated documentation files (the "Software"), to deal
	* in the Software without restriction, including without limitation the rights
	* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	* copies of the Software, and to permit persons to whom the Software is
	* furnished to do so, subject to the following conditions:
	*
	* The above copyright notice and this permission notice shall be included in
	* all copies or substantial portions of the Software.
	*
	* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
	* THE SOFTWARE.
	*/
	var VNode = __webpack_require__(68)
	  , VText = __webpack_require__(69)
	  , VComment = __webpack_require__(70)

	module.exports = createVNode

	function createVNode(domNode, key) {
	  key = key || null // XXX: Leave out `key` for now... merely used for (re-)ordering

	  if(domNode.nodeType == 1) return createFromElement(domNode, key)
	  if(domNode.nodeType == 3) return createFromTextNode(domNode, key)
	  if(domNode.nodeType == 8) return createFromCommentNode(domNode, key)
	  return
	}

	function createFromTextNode(tNode) {
	  return new VText(tNode.nodeValue)
	}


	function createFromCommentNode(cNode) {
	  return new VComment(cNode.nodeValue)
	}


	function createFromElement(el) {
	  var tagName = el.tagName
	  , namespace = el.namespaceURI == 'http://www.w3.org/1999/xhtml'? null : el.namespaceURI
	  , properties = getElementProperties(el)
	  , children = []

	  for (var i = 0; i < el.childNodes.length; i++) {
	    children.push(createVNode(el.childNodes[i]/*, i*/))
	  }

	  return new VNode(tagName, properties, children, null, namespace)
	}


	function getElementProperties(el) {
	  var obj = {}

	  for(var i=0; i<props.length; i++) {
	    var propName = props[i]
	    if(!el[propName]) continue

	    // Special case: style
	    // .style is a DOMStyleDeclaration, thus we need to iterate over all
	    // rules to create a hash of applied css properties.
	    //
	    // You can directly set a specific .style[prop] = value so patching with vdom
	    // is possible.
	    if("style" == propName) {
	      var css = {}
	        , styleProp
	      if ('undefined' !== typeof el.style.length) {
	        for(var j=0; j<el.style.length; j++) {
	          styleProp = el.style[j]
	          css[styleProp] = el.style.getPropertyValue(styleProp) // XXX: add support for "!important" via getPropertyPriority()!
	        }
	      } else { // IE8
	        for (var styleProp in el.style) {
	          if (el.style[styleProp] && el.style.hasOwnProperty(styleProp)) {
	            css[styleProp] = el.style[styleProp];
	          }
	        }
	      }

	      if(Object.keys(css).length) obj[propName] = css
	      continue
	    }

	    // https://msdn.microsoft.com/en-us/library/cc848861%28v=vs.85%29.aspx
	    // The img element does not support the HREF content attribute.
	    // In addition, the href property is read-only for the img Document Object Model (DOM) object
	    if (el.tagName.toLowerCase() === 'img' && propName === 'href') {
	      continue;
	    }

	    // Special case: dataset
	    // we can iterate over .dataset with a simple for..in loop.
	    // The all-time foo with data-* attribs is the dash-snake to camelCase
	    // conversion.
	    //
	    // *This is compatible with h(), but not with every browser, thus this section was removed in favor
	    // of attributes (specified below)!*
	    //
	    // .dataset properties are directly accessible as transparent getters/setters, so
	    // patching with vdom is possible.
	    /*if("dataset" == propName) {
	      var data = {}
	      for(var p in el.dataset) {
	        data[p] = el.dataset[p]
	      }
	      obj[propName] = data
	      return
	    }*/

	    // Special case: attributes
	    // these are a NamedNodeMap, but we can just convert them to a hash for vdom,
	    // because of https://github.com/Matt-Esch/virtual-dom/blob/master/vdom/apply-properties.js#L57
	    if("attributes" == propName){
	      var atts = Array.prototype.slice.call(el[propName]);
	      var hash = {}
	      for(var k=0; k<atts.length; k++){
	        var name = atts[k].name;
	        if(obj[name] || obj[attrBlacklist[name]]) continue;
	        hash[name] = el.getAttribute(name);
	      }
	      obj[propName] = hash;
	      continue
	    }
	    if("tabIndex" == propName && el.tabIndex === -1) continue

	    // Special case: contentEditable
	    // browser use 'inherit' by default on all nodes, but does not allow setting it to ''
	    // diffing virtualize dom will trigger error
	    // ref: https://github.com/Matt-Esch/virtual-dom/issues/176
	    if("contentEditable" == propName && el[propName] === 'inherit') continue

	    if('object' === typeof el[propName]) continue

	    // default: just copy the property
	    obj[propName] = el[propName]
	  }

	  return obj
	}

	/**
	 * DOMNode property white list
	 * Taken from https://github.com/Raynos/react/blob/dom-property-config/src/browser/ui/dom/DefaultDOMPropertyConfig.js
	 */
	var props =

	module.exports.properties = [
	 "accept"
	,"accessKey"
	,"action"
	,"alt"
	,"async"
	,"autoComplete"
	,"autoPlay"
	,"cellPadding"
	,"cellSpacing"
	,"checked"
	,"className"
	,"colSpan"
	,"content"
	,"contentEditable"
	,"controls"
	,"crossOrigin"
	,"data"
	//,"dataset" removed since attributes handles data-attributes
	,"defer"
	,"dir"
	,"download"
	,"draggable"
	,"encType"
	,"formNoValidate"
	,"href"
	,"hrefLang"
	,"htmlFor"
	,"httpEquiv"
	,"icon"
	,"id"
	,"label"
	,"lang"
	,"list"
	,"loop"
	,"max"
	,"mediaGroup"
	,"method"
	,"min"
	,"multiple"
	,"muted"
	,"name"
	,"noValidate"
	,"pattern"
	,"placeholder"
	,"poster"
	,"preload"
	,"radioGroup"
	,"readOnly"
	,"rel"
	,"required"
	,"rowSpan"
	,"sandbox"
	,"scope"
	,"scrollLeft"
	,"scrolling"
	,"scrollTop"
	,"selected"
	,"span"
	,"spellCheck"
	,"src"
	,"srcDoc"
	,"srcSet"
	,"start"
	,"step"
	,"style"
	,"tabIndex"
	,"target"
	,"title"
	,"type"
	,"value"

	// Non-standard Properties
	,"autoCapitalize"
	,"autoCorrect"
	,"property"

	, "attributes"
	]

	var attrBlacklist =
	module.exports.attrBlacklist = {
	  'class': 'className'
	}


/***/ },
/* 68 */
/***/ function(module, exports, __webpack_require__) {

	var version = __webpack_require__(48)
	var isVNode = __webpack_require__(49)
	var isWidget = __webpack_require__(51)
	var isThunk = __webpack_require__(52)
	var isVHook = __webpack_require__(56)

	module.exports = VirtualNode

	var noProperties = {}
	var noChildren = []

	function VirtualNode(tagName, properties, children, key, namespace) {
	    this.tagName = tagName
	    this.properties = properties || noProperties
	    this.children = children || noChildren
	    this.key = key != null ? String(key) : undefined
	    this.namespace = (typeof namespace === "string") ? namespace : null

	    var count = (children && children.length) || 0
	    var descendants = 0
	    var hasWidgets = false
	    var hasThunks = false
	    var descendantHooks = false
	    var hooks

	    for (var propName in properties) {
	        if (properties.hasOwnProperty(propName)) {
	            var property = properties[propName]
	            if (isVHook(property) && property.unhook) {
	                if (!hooks) {
	                    hooks = {}
	                }

	                hooks[propName] = property
	            }
	        }
	    }

	    for (var i = 0; i < count; i++) {
	        var child = children[i]
	        if (isVNode(child)) {
	            descendants += child.count || 0

	            if (!hasWidgets && child.hasWidgets) {
	                hasWidgets = true
	            }

	            if (!hasThunks && child.hasThunks) {
	                hasThunks = true
	            }

	            if (!descendantHooks && (child.hooks || child.descendantHooks)) {
	                descendantHooks = true
	            }
	        } else if (!hasWidgets && isWidget(child)) {
	            if (typeof child.destroy === "function") {
	                hasWidgets = true
	            }
	        } else if (!hasThunks && isThunk(child)) {
	            hasThunks = true;
	        }
	    }

	    this.count = count + descendants
	    this.hasWidgets = hasWidgets
	    this.hasThunks = hasThunks
	    this.hooks = hooks
	    this.descendantHooks = descendantHooks
	}

	VirtualNode.prototype.version = version
	VirtualNode.prototype.type = "VirtualNode"


/***/ },
/* 69 */
/***/ function(module, exports, __webpack_require__) {

	var version = __webpack_require__(48)

	module.exports = VirtualText

	function VirtualText(text) {
	    this.text = String(text)
	}

	VirtualText.prototype.version = version
	VirtualText.prototype.type = "VirtualText"


/***/ },
/* 70 */
/***/ function(module, exports) {

	module.exports = VirtualComment

	function VirtualComment(text) {
	  this.text = String(text)
	}

	VirtualComment.prototype.type = 'Widget'

	VirtualComment.prototype.init = function() {
	  return document.createComment(this.text)
	}

	VirtualComment.prototype.update = function(previous, domNode) {
	  if(this.text === previous.text) return
	  domNode.nodeValue = this.text
	}


/***/ },
/* 71 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable object-shorthand */
	__webpack_require__(10);

	var eventRegExp = /^(\S+) (.*)$/;

	module.exports = {
	    events: {
	        click: {},
	        change: {},
	        keyup: {},
	        submit: {}
	    },

	    init: function init(fn) {
	        fn.call(this);
	    },

	    observe: function observer(el) {
	        var _this = this;

	        this.el = el;
	        Object.keys(this.events).forEach(function (type) {
	            _this.el.addEventListener(type, _this.delegate(type));
	        });
	    },

	    add: function add(obj) {
	        var _this2 = this;

	        Object.keys(obj).forEach(function (query) {
	            var fn = obj[query];
	            var match = query.match(eventRegExp);
	            var type = match ? match[1] : query;
	            var selector = match ? match[2] : '';
	            _this2.events[type][selector] = fn;
	        });
	        return obj;
	    },

	    delegate: function delegate(type) {
	        var _this3 = this;

	        return function (e) {
	            var el = e.target;
	            while (el && el !== _this3.el) {
	                Object.keys(_this3.events[type]).forEach(function (selector) {
	                    var fn = _this3.events[type][selector];
	                    if (el.matches(selector)) {
	                        fn.call(_this3, e, el);
	                    }
	                });
	                el = el.parentNode;
	            }
	        };
	    }
	};

/***/ },
/* 72 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch;

	var tasks = __webpack_require__(73);
	var qs = __webpack_require__(74);
	var pageTitles = __webpack_require__(75);

	var _require2 = __webpack_require__(7),
	    matchesRoute = _require2.matchesRoute;

	var request = function request() {
	    return window.location.pathname + window.location.search;
	};

	var getQueryParams = function getQueryParams(path) {
	    if (path.indexOf('?') === -1) {
	        return {};
	    }
	    return qs.get(path.split('?')[1]);
	};

	var findTitle = function findTitle(path) {
	    for (var i = 0; i < pageTitles.length; i++) {
	        var _route = pageTitles[i];
	        var args = matchesRoute(path, _route.path);
	        if (args) {
	            return _route.title;
	        }
	    }
	};

	var _route2 = function _route2(path) {
	    dispatch({
	        type: 'SET_ROUTE',
	        route: path,
	        routeQuery: getQueryParams(path),
	        title: findTitle(path)
	    });
	    if (tasks.onRoute) {
	        return tasks.onRoute(path);
	    }
	};

	if (typeof window !== 'undefined') {
	    window.onpopstate = function () {
	        _route2(request());
	    };
	}

	tasks.add({
	    route: function route(path) {
	        if (path !== request()) {
	            history.pushState({}, '', path);
	            _route2(path);
	        }
	    }
	});

	module.exports = { route: _route2 };

/***/ },
/* 73 */
/***/ function(module, exports) {

	"use strict";

	var tasks = {};
	tasks.add = function addTasks(givenTasks) {
	    Object.keys(givenTasks).forEach(function (key) {
	        tasks[key] = givenTasks[key];
	    });
	    return givenTasks;
	};
	module.exports = tasks;

/***/ },
/* 74 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

	var _require = __webpack_require__(7),
	    valuefy = _require.valuefy;

	var get = function get(query) {
	    query = query || typeof window !== 'undefined' && window.location.search.substring(1);
	    if (!query) {
	        return {};
	    }
	    var params = query.split('&');
	    var data = {};
	    params.forEach(function (param) {
	        var _param$split = param.split('='),
	            _param$split2 = _slicedToArray(_param$split, 2),
	            key = _param$split2[0],
	            value = _param$split2[1];

	        data[decodeURIComponent(key)] = valuefy(value);
	    });
	    return data;
	};

	module.exports = { valuefy: valuefy, get: get };

/***/ },
/* 75 */
/***/ function(module, exports) {

	'use strict';

	var routes = [{
	    path: '/sign_up',
	    title: 'Sign Up'
	}, {
	    path: '/log_in',
	    title: 'Log In'
	}, {
	    path: '/password',
	    title: 'Password'
	}, {
	    path: '/styleguide',
	    title: 'Styleguide'
	}, {
	    path: '/terms',
	    title: 'Privacy & Terms'
	}, {
	    path: '/contact',
	    title: 'Contact'
	}, {
	    path: '/settings',
	    title: 'Settings'
	}, {
	    path: '/notices',
	    title: 'Notices'
	}, {
	    path: '/search',
	    title: 'Search'
	}, {
	    path: '/create/subject/create',
	    title: 'Create a New Subject'
	}, {
	    path: '/create/subject/add',
	    title: 'Add Existing Members to a Subject'
	}, {
	    path: '/create/unit/find',
	    title: 'Find a Subject to Add Units'
	}, {
	    path: '/create/unit/list',
	    title: 'Add Units to Subject'
	}, {
	    path: '/create/unit/add',
	    title: 'Add Existing Unit to Subject'
	}, {
	    path: '/create/unit/create/add',
	    title: 'Find Requires for New Unit'
	}, {
	    path: '/create/unit/create',
	    title: 'Create a New Unit for Subject'
	}, {
	    path: '/create/card/find',
	    title: 'Find a Unit to Add Cards'
	}, {
	    path: '/create/card/list',
	    title: 'Add Cards to Unit'
	}, {
	    path: '/create/card/create',
	    title: 'Create a New Card for Unit'
	}, {
	    path: '/create',
	    title: 'Create'
	}, {
	    path: /^\/topics\/(create|[\d\w\-_]+\/update)$/,
	    title: 'Topic'
	    // Must be before `topic`
	}, {
	    path: '/topics/{id}/posts/create',
	    title: 'Create Post'
	}, {
	    path: '/topics/{id}/posts/{id}/update',
	    title: 'Update Post'
	}, {
	    path: '/topics/{id}',
	    title: 'Topic'
	}, {
	    path: '/users/{id}',
	    title: 'Profile'
	}, {
	    path: '/cards/{id}',
	    title: 'Card'
	}, {
	    path: '/units/{id}',
	    title: 'Unit'
	}, {
	    path: '/subjects/{id}',
	    title: 'Subject'
	}, {
	    path: /^\/(card|unit|subject)s\/([\w\d-]+)\/versions$/,
	    title: 'Versions'
	}, {
	    path: '/follows',
	    title: 'Follows'
	}, {
	    path: '/recommended_subjects',
	    title: 'Recommended Subjects'
	}, {
	    path: '/my_subjects',
	    title: 'My Subjects'
	}, {
	    path: '/subjects/{id}/tree',
	    title: 'Subject Tree'
	}, {
	    path: '/subjects/{id}/choose_unit',
	    title: 'Choose Unit'
	}, {
	    path: '/cards/{id}/learn',
	    title: 'Learn'
	}, {
	    path: '/subjects/{id}/landing',
	    title: 'An Introduction to Electronic Music'
	}, {
	    path: /^\/suggest.*$/,
	    title: 'Suggest free online learning experiences'
	}, {
	    path: /^\/?$/,
	    title: 'Home'
	    // Must be 2nd to last
	}, {
	    path: /.*/,
	    title: '404'
	    // Must be last
	}];

	module.exports = routes;

/***/ },
/* 76 */
/***/ function(module, exports) {

	'use strict';

	var _arguments = arguments;
	var ga = window.ga = window.ga || function () {
	    window.ga.q = window.ga.q || [];
	    window.ga.q.push(_arguments);
	};

	var startGoogleAnalytics = function startGoogleAnalytics() {
	    window.GoogleAnalyticsObject = 'ga';
	    window.ga.l = 1 * new Date();
	    var a = document.createElement('script');
	    a.async = 1;
	    a.src = '//www.google-analytics.com/analytics.js';
	    var m = document.getElementsByTagName('script')[0];
	    if (m) {
	        m.parentNode.insertBefore(a, m);
	    }
	    if (!m) {
	        document.body.appendChild(a);
	    }

	    ga('create', 'UA-40497674-1', 'auto');
	    ga('send', 'pageview');
	};

	var trackEvent = function trackEvent(action) {
	    if (action.type === 'SET_ROUTE') {
	        ga('send', {
	            hitType: 'pageview',
	            page: action.route
	        });
	        ga('set', {
	            page: action.route
	        });
	    } else {
	        ga('send', {
	            hitType: 'event',
	            eventCategory: 'Sagefy',
	            eventAction: action.type,
	            eventLabel: JSON.stringify(action)
	        });
	    }
	};

	module.exports = { startGoogleAnalytics: startGoogleAnalytics, trackEvent: trackEvent };

/***/ },
/* 77 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

	/* eslint-disable global-require */
	var _require = __webpack_require__(7),
	    matchesRoute = _require.matchesRoute;

	var _require2 = __webpack_require__(78),
	    div = _require2.div,
	    main = _require2.main;

	var _require3 = __webpack_require__(9

	/*
	TODO-3 distribute routing, something like...
	     module.exports = route(/^\/?$/, 'Home', (data) =>)
	*/

	),
	    copy = _require3.copy;

	var routes = [{
	    path: '/sign_up',
	    tmpl: __webpack_require__(88)
	}, {
	    path: '/log_in',
	    tmpl: __webpack_require__(111)
	}, {
	    path: '/password',
	    tmpl: __webpack_require__(112)
	}, {
	    path: '/styleguide',
	    tmpl: __webpack_require__(114)
	}, {
	    path: '/terms',
	    tmpl: __webpack_require__(116)
	}, {
	    path: '/contact',
	    tmpl: __webpack_require__(118)
	}, {
	    path: '/settings',
	    tmpl: __webpack_require__(119)
	}, {
	    path: '/notices',
	    tmpl: __webpack_require__(121)
	}, {
	    path: '/search',
	    tmpl: __webpack_require__(124)
	}, {
	    path: '/create/subject/create',
	    tmpl: __webpack_require__(125)
	}, {
	    path: '/create/subject/add',
	    tmpl: __webpack_require__(127)
	}, {
	    path: '/create/unit/find',
	    tmpl: __webpack_require__(128)
	}, {
	    path: '/create/unit/list',
	    tmpl: __webpack_require__(130)
	}, {
	    path: '/create/unit/add',
	    tmpl: __webpack_require__(131)
	}, {
	    path: '/create/unit/create/add',
	    tmpl: __webpack_require__(132)
	}, {
	    path: '/create/unit/create',
	    tmpl: __webpack_require__(133)
	}, {
	    path: '/create/card/find',
	    tmpl: __webpack_require__(135)
	}, {
	    path: '/create/card/list',
	    tmpl: __webpack_require__(136)
	}, {
	    path: '/create/card/create',
	    tmpl: __webpack_require__(137)
	}, {
	    path: '/create',
	    tmpl: __webpack_require__(141)
	}, {
	    path: /^\/topics\/(create|[\d\w\-_]+\/update)$/,
	    tmpl: __webpack_require__(143)
	    // Must be before `topic`
	}, {
	    path: '/topics/{id}/posts/create',
	    tmpl: __webpack_require__(149)
	}, {
	    path: '/topics/{id}/posts/{id}/update',
	    tmpl: __webpack_require__(149)
	}, {
	    path: '/topics/{id}',
	    tmpl: __webpack_require__(150)
	}, {
	    path: '/users/{id}',
	    tmpl: __webpack_require__(159)
	}, {
	    path: '/cards/{id}',
	    tmpl: __webpack_require__(160)
	}, {
	    path: '/units/{id}',
	    tmpl: __webpack_require__(165)
	}, {
	    path: '/subjects/{id}',
	    tmpl: __webpack_require__(166)
	}, {
	    path: /^\/(card|unit|subject)s\/([\w\d-_]+)\/versions$/,
	    tmpl: __webpack_require__(167)
	}, {
	    path: '/follows',
	    tmpl: __webpack_require__(168)
	}, {
	    path: '/recommended_subjects',
	    tmpl: __webpack_require__(169)
	}, {
	    path: '/my_subjects',
	    tmpl: __webpack_require__(170)
	}, {
	    path: '/subjects/{id}/tree',
	    tmpl: __webpack_require__(171)
	}, {
	    path: '/subjects/{id}/choose_unit',
	    tmpl: __webpack_require__(177)
	}, {
	    path: '/cards/{id}/learn',
	    tmpl: __webpack_require__(178)
	}, {
	    path: '/subjects/{id}/landing',
	    tmpl: __webpack_require__(181)
	}, {
	    path: /^\/suggest.*$/,
	    tmpl: __webpack_require__(182)
	}, {
	    path: /^\/?$/,
	    tmpl: __webpack_require__(183)
	    // Must be 2nd to last
	}, {
	    path: /.*/,
	    tmpl: __webpack_require__(184)
	    // Must be last
	}];

	var findRouteTmpl = function findRouteTmpl(data) {
	    for (var i = 0; i < routes.length; i++) {
	        var route = routes[i];
	        var args = matchesRoute(data.route, route.path);
	        if (args) {
	            return [route.tmpl, args];
	        }
	    }
	};

	module.exports = function (data) {
	    var menuData = copy(data.menu);
	    menuData.kind = data.currentUserID ? 'loggedIn' : 'loggedOut';

	    var _findRouteTmpl = findRouteTmpl(data),
	        _findRouteTmpl2 = _slicedToArray(_findRouteTmpl, 2),
	        route = _findRouteTmpl2[0],
	        args = _findRouteTmpl2[1];

	    data = copy(data);
	    data.routeArgs = args;
	    return div(main(route(data)), __webpack_require__(185)(menuData), __webpack_require__(187) // TODO-2 Remove this component
	    ());
	};

/***/ },
/* 78 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var h = __webpack_require__(79);

	var names = [
	// Super elements
	'meta',

	// Block-level layout elements
	'article', 'nav', 'aside', 'section', 'header', 'footer',

	// Other block-level elements
	'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'main', 'address', 'p', 'hr', 'pre', 'blockquote', 'ol', 'ul', 'li', 'dl', 'dt', 'dd', 'figure', 'figcaption', 'div', 'br', 'hgroup',

	// Table elements
	'table', 'caption', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td', 'col', 'colgroup',

	// Form elements
	'form', 'fieldset', 'legend', 'label', 'input', 'button', 'select', 'datalist', 'optgroup', 'option', 'textarea', 'output', 'progress', 'meter',

	// Media elements
	'img', 'iframe', 'embed', 'object', 'param', 'video', 'audio', 'source', 'canvas', 'track',

	// Inline elements
	'a', 'em', 'strong', 'i', 'small', 'abbr', 'del', 'ins', 'q', 'cite', 'dfn', 'sub', 'sup', 'time', 'code', 'kbd', 'samp', 'var', 'mark', 'span'];

	var tags = {};
	var objConstructor = {}.constructor;
	names.forEach(function (name) {
	    tags[name] = function () {
	        for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
	            args[_key] = arguments[_key];
	        }

	        if (args.length === 0) {
	            return h(name);
	        }
	        if (args[0] && args[0].constructor === objConstructor) {
	            return h(name, args[0], args.slice(1));
	        }
	        return h(name, args);
	    };
	});

	module.exports = tags;

/***/ },
/* 79 */
/***/ function(module, exports, __webpack_require__) {

	var h = __webpack_require__(80)

	module.exports = h


/***/ },
/* 80 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var isArray = __webpack_require__(46);

	var VNode = __webpack_require__(68);
	var VText = __webpack_require__(69);
	var isVNode = __webpack_require__(49);
	var isVText = __webpack_require__(50);
	var isWidget = __webpack_require__(51);
	var isHook = __webpack_require__(56);
	var isVThunk = __webpack_require__(52);

	var parseTag = __webpack_require__(81);
	var softSetHook = __webpack_require__(83);
	var evHook = __webpack_require__(84);

	module.exports = h;

	function h(tagName, properties, children) {
	    var childNodes = [];
	    var tag, props, key, namespace;

	    if (!children && isChildren(properties)) {
	        children = properties;
	        props = {};
	    }

	    props = props || properties || {};
	    tag = parseTag(tagName, props);

	    // support keys
	    if (props.hasOwnProperty('key')) {
	        key = props.key;
	        props.key = undefined;
	    }

	    // support namespace
	    if (props.hasOwnProperty('namespace')) {
	        namespace = props.namespace;
	        props.namespace = undefined;
	    }

	    // fix cursor bug
	    if (tag === 'INPUT' &&
	        !namespace &&
	        props.hasOwnProperty('value') &&
	        props.value !== undefined &&
	        !isHook(props.value)
	    ) {
	        props.value = softSetHook(props.value);
	    }

	    transformProperties(props);

	    if (children !== undefined && children !== null) {
	        addChild(children, childNodes, tag, props);
	    }


	    return new VNode(tag, props, childNodes, key, namespace);
	}

	function addChild(c, childNodes, tag, props) {
	    if (typeof c === 'string') {
	        childNodes.push(new VText(c));
	    } else if (typeof c === 'number') {
	        childNodes.push(new VText(String(c)));
	    } else if (isChild(c)) {
	        childNodes.push(c);
	    } else if (isArray(c)) {
	        for (var i = 0; i < c.length; i++) {
	            addChild(c[i], childNodes, tag, props);
	        }
	    } else if (c === null || c === undefined) {
	        return;
	    } else {
	        throw UnexpectedVirtualElement({
	            foreignObject: c,
	            parentVnode: {
	                tagName: tag,
	                properties: props
	            }
	        });
	    }
	}

	function transformProperties(props) {
	    for (var propName in props) {
	        if (props.hasOwnProperty(propName)) {
	            var value = props[propName];

	            if (isHook(value)) {
	                continue;
	            }

	            if (propName.substr(0, 3) === 'ev-') {
	                // add ev-foo support
	                props[propName] = evHook(value);
	            }
	        }
	    }
	}

	function isChild(x) {
	    return isVNode(x) || isVText(x) || isWidget(x) || isVThunk(x);
	}

	function isChildren(x) {
	    return typeof x === 'string' || isArray(x) || isChild(x);
	}

	function UnexpectedVirtualElement(data) {
	    var err = new Error();

	    err.type = 'virtual-hyperscript.unexpected.virtual-element';
	    err.message = 'Unexpected virtual child passed to h().\n' +
	        'Expected a VNode / Vthunk / VWidget / string but:\n' +
	        'got:\n' +
	        errorString(data.foreignObject) +
	        '.\n' +
	        'The parent vnode is:\n' +
	        errorString(data.parentVnode)
	        '\n' +
	        'Suggested fix: change your `h(..., [ ... ])` callsite.';
	    err.foreignObject = data.foreignObject;
	    err.parentVnode = data.parentVnode;

	    return err;
	}

	function errorString(obj) {
	    try {
	        return JSON.stringify(obj, null, '    ');
	    } catch (e) {
	        return String(obj);
	    }
	}


/***/ },
/* 81 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var split = __webpack_require__(82);

	var classIdSplit = /([\.#]?[a-zA-Z0-9\u007F-\uFFFF_:-]+)/;
	var notClassId = /^\.|#/;

	module.exports = parseTag;

	function parseTag(tag, props) {
	    if (!tag) {
	        return 'DIV';
	    }

	    var noId = !(props.hasOwnProperty('id'));

	    var tagParts = split(tag, classIdSplit);
	    var tagName = null;

	    if (notClassId.test(tagParts[1])) {
	        tagName = 'DIV';
	    }

	    var classes, part, type, i;

	    for (i = 0; i < tagParts.length; i++) {
	        part = tagParts[i];

	        if (!part) {
	            continue;
	        }

	        type = part.charAt(0);

	        if (!tagName) {
	            tagName = part;
	        } else if (type === '.') {
	            classes = classes || [];
	            classes.push(part.substring(1, part.length));
	        } else if (type === '#' && noId) {
	            props.id = part.substring(1, part.length);
	        }
	    }

	    if (classes) {
	        if (props.className) {
	            classes.push(props.className);
	        }

	        props.className = classes.join(' ');
	    }

	    return props.namespace ? tagName : tagName.toUpperCase();
	}


/***/ },
/* 82 */
/***/ function(module, exports) {

	/*!
	 * Cross-Browser Split 1.1.1
	 * Copyright 2007-2012 Steven Levithan <stevenlevithan.com>
	 * Available under the MIT License
	 * ECMAScript compliant, uniform cross-browser split method
	 */

	/**
	 * Splits a string into an array of strings using a regex or string separator. Matches of the
	 * separator are not included in the result array. However, if `separator` is a regex that contains
	 * capturing groups, backreferences are spliced into the result each time `separator` is matched.
	 * Fixes browser bugs compared to the native `String.prototype.split` and can be used reliably
	 * cross-browser.
	 * @param {String} str String to split.
	 * @param {RegExp|String} separator Regex or string to use for separating the string.
	 * @param {Number} [limit] Maximum number of items to include in the result array.
	 * @returns {Array} Array of substrings.
	 * @example
	 *
	 * // Basic use
	 * split('a b c d', ' ');
	 * // -> ['a', 'b', 'c', 'd']
	 *
	 * // With limit
	 * split('a b c d', ' ', 2);
	 * // -> ['a', 'b']
	 *
	 * // Backreferences in result array
	 * split('..word1 word2..', /([a-z]+)(\d+)/i);
	 * // -> ['..', 'word', '1', ' ', 'word', '2', '..']
	 */
	module.exports = (function split(undef) {

	  var nativeSplit = String.prototype.split,
	    compliantExecNpcg = /()??/.exec("")[1] === undef,
	    // NPCG: nonparticipating capturing group
	    self;

	  self = function(str, separator, limit) {
	    // If `separator` is not a regex, use `nativeSplit`
	    if (Object.prototype.toString.call(separator) !== "[object RegExp]") {
	      return nativeSplit.call(str, separator, limit);
	    }
	    var output = [],
	      flags = (separator.ignoreCase ? "i" : "") + (separator.multiline ? "m" : "") + (separator.extended ? "x" : "") + // Proposed for ES6
	      (separator.sticky ? "y" : ""),
	      // Firefox 3+
	      lastLastIndex = 0,
	      // Make `global` and avoid `lastIndex` issues by working with a copy
	      separator = new RegExp(separator.source, flags + "g"),
	      separator2, match, lastIndex, lastLength;
	    str += ""; // Type-convert
	    if (!compliantExecNpcg) {
	      // Doesn't need flags gy, but they don't hurt
	      separator2 = new RegExp("^" + separator.source + "$(?!\\s)", flags);
	    }
	    /* Values for `limit`, per the spec:
	     * If undefined: 4294967295 // Math.pow(2, 32) - 1
	     * If 0, Infinity, or NaN: 0
	     * If positive number: limit = Math.floor(limit); if (limit > 4294967295) limit -= 4294967296;
	     * If negative number: 4294967296 - Math.floor(Math.abs(limit))
	     * If other: Type-convert, then use the above rules
	     */
	    limit = limit === undef ? -1 >>> 0 : // Math.pow(2, 32) - 1
	    limit >>> 0; // ToUint32(limit)
	    while (match = separator.exec(str)) {
	      // `separator.lastIndex` is not reliable cross-browser
	      lastIndex = match.index + match[0].length;
	      if (lastIndex > lastLastIndex) {
	        output.push(str.slice(lastLastIndex, match.index));
	        // Fix browsers whose `exec` methods don't consistently return `undefined` for
	        // nonparticipating capturing groups
	        if (!compliantExecNpcg && match.length > 1) {
	          match[0].replace(separator2, function() {
	            for (var i = 1; i < arguments.length - 2; i++) {
	              if (arguments[i] === undef) {
	                match[i] = undef;
	              }
	            }
	          });
	        }
	        if (match.length > 1 && match.index < str.length) {
	          Array.prototype.push.apply(output, match.slice(1));
	        }
	        lastLength = match[0].length;
	        lastLastIndex = lastIndex;
	        if (output.length >= limit) {
	          break;
	        }
	      }
	      if (separator.lastIndex === match.index) {
	        separator.lastIndex++; // Avoid an infinite loop
	      }
	    }
	    if (lastLastIndex === str.length) {
	      if (lastLength || !separator.test("")) {
	        output.push("");
	      }
	    } else {
	      output.push(str.slice(lastLastIndex));
	    }
	    return output.length > limit ? output.slice(0, limit) : output;
	  };

	  return self;
	})();


/***/ },
/* 83 */
/***/ function(module, exports) {

	'use strict';

	module.exports = SoftSetHook;

	function SoftSetHook(value) {
	    if (!(this instanceof SoftSetHook)) {
	        return new SoftSetHook(value);
	    }

	    this.value = value;
	}

	SoftSetHook.prototype.hook = function (node, propertyName) {
	    if (node[propertyName] !== this.value) {
	        node[propertyName] = this.value;
	    }
	};


/***/ },
/* 84 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var EvStore = __webpack_require__(85);

	module.exports = EvHook;

	function EvHook(value) {
	    if (!(this instanceof EvHook)) {
	        return new EvHook(value);
	    }

	    this.value = value;
	}

	EvHook.prototype.hook = function (node, propertyName) {
	    var es = EvStore(node);
	    var propName = propertyName.substr(3);

	    es[propName] = this.value;
	};

	EvHook.prototype.unhook = function(node, propertyName) {
	    var es = EvStore(node);
	    var propName = propertyName.substr(3);

	    es[propName] = undefined;
	};


/***/ },
/* 85 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var OneVersionConstraint = __webpack_require__(86);

	var MY_VERSION = '7';
	OneVersionConstraint('ev-store', MY_VERSION);

	var hashKey = '__EV_STORE_KEY@' + MY_VERSION;

	module.exports = EvStore;

	function EvStore(elem) {
	    var hash = elem[hashKey];

	    if (!hash) {
	        hash = elem[hashKey] = {};
	    }

	    return hash;
	}


/***/ },
/* 86 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var Individual = __webpack_require__(87);

	module.exports = OneVersion;

	function OneVersion(moduleName, version, defaultValue) {
	    var key = '__INDIVIDUAL_ONE_VERSION_' + moduleName;
	    var enforceKey = key + '_ENFORCE_SINGLETON';

	    var versionValue = Individual(enforceKey, version);

	    if (versionValue !== version) {
	        throw new Error('Can only have one copy of ' +
	            moduleName + '.\n' +
	            'You already have version ' + versionValue +
	            ' installed.\n' +
	            'This means you cannot install version ' + version);
	    }

	    return Individual(key, defaultValue);
	}


/***/ },
/* 87 */
/***/ function(module, exports) {

	/* WEBPACK VAR INJECTION */(function(global) {'use strict';

	/*global window, global*/

	var root = typeof window !== 'undefined' ?
	    window : typeof global !== 'undefined' ?
	    global : {};

	module.exports = Individual;

	function Individual(key, value) {
	    if (key in root) {
	        return root[key];
	    }

	    root[key] = value;

	    return value;
	}

	/* WEBPACK VAR INJECTION */}.call(exports, (function() { return this; }())))

/***/ },
/* 88 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    p = _require.p,
	    a = _require.a,
	    br = _require.br;

	var form = __webpack_require__(89);
	var icon = __webpack_require__(91);
	var userSchema = __webpack_require__(110);

	var _require2 = __webpack_require__(9),
	    extend = _require2.extend;

	var _require3 = __webpack_require__(7),
	    createFieldsData = _require3.createFieldsData,
	    findGlobalErrors = _require3.findGlobalErrors;

	var fields = [{
	    name: 'name',
	    label: 'Name',
	    placeholder: 'ex: Unicorn'
	}, {
	    name: 'email',
	    label: 'Email',
	    description: 'We need your email to send notices ' + 'and to reset your password.',
	    placeholder: 'ex: unicorn@example.com'
	}, {
	    name: 'password',
	    label: 'Password'
	}, {
	    name: 'submit',
	    label: 'Sign Up',
	    type: 'submit',
	    icon: 'sign-up'
	}];

	fields.forEach(function (field, index) {
	    fields[index] = extend({}, userSchema[field.name] || {}, field);
	});

	module.exports = function (data) {
	    if (data.currentUserID) {
	        return div('Logged in already.');
	    }

	    var instanceFields = createFieldsData({
	        schema: userSchema,
	        fields: fields,
	        errors: data.errors,
	        formData: data.formData,
	        sending: data.sending
	    });

	    var globalErrors = findGlobalErrors({
	        fields: fields,
	        errors: data.errors
	    });

	    return div({ id: 'sign-up', className: 'page' }, h1('Sign Up'), p('Already have an account? ', a({ href: '/log_in' }, icon('log-in'), ' Log In'), '.', br(), 'By signing up, you agree to our ', a({ href: '/terms' }, icon('terms'), ' Terms of Service'), '.'), form({
	        fields: instanceFields,
	        errors: globalErrors
	    }));
	};

/***/ },
/* 89 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    form = _require.form,
	    ul = _require.ul;

	var formField = __webpack_require__(90);
	var formError = __webpack_require__(109);

	module.exports = function (_ref) {
	    var fields = _ref.fields,
	        errors = _ref.errors;
	    return form(fields.map(function (field) {
	        return formField(field);
	    }), errors && errors.length ? ul({ className: 'form__errors' }, errors.map(function (error) {
	        return formError(error);
	    })) : null);
	};

/***/ },
/* 90 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    p = _require.p,
	    span = _require.span;

	var icon = __webpack_require__(91);

	var kindTmpl = {};
	kindTmpl.label = __webpack_require__(92);
	kindTmpl.input = __webpack_require__(97);
	kindTmpl.textarea = __webpack_require__(98);
	kindTmpl.button = __webpack_require__(99);
	kindTmpl.select = __webpack_require__(100);
	kindTmpl.list = __webpack_require__(102);
	kindTmpl.entities = __webpack_require__(103);

	module.exports = function (data) {
	    var classes = ['form-field', 'form-field--' + data.type, 'form-field--' + data.name, data.error ? 'form-field--bad' : '', data.good ? 'form-field--good' : ''].join(' ');
	    return div({ className: classes }, m(data));
	};

	var m = function m(data) {
	    var nodes = [];
	    if (data.label && ['button', 'submit'].indexOf(data.type) === -1) {
	        nodes.push(kindTmpl.label(data));
	    }
	    if (['text', 'email', 'number', 'password', 'hidden'].indexOf(data.type) > -1) {
	        nodes.push(kindTmpl.input(data));
	    }
	    if (data.type === 'textarea') {
	        nodes.push(kindTmpl.textarea(data));
	    }
	    if (['submit', 'button'].indexOf(data.type) > -1) {
	        nodes.push(kindTmpl.button(data));
	    }
	    if (data.type === 'select') {
	        nodes.push(kindTmpl.select(data));
	    }
	    if (data.type === 'list') {
	        nodes.push(kindTmpl.list(data));
	    }
	    if (data.type === 'entities') {
	        nodes.push(kindTmpl.entities(data));
	    }
	    if (data.error) {
	        nodes.push(span({ className: 'form-field__feedback' }, icon('bad'), data.error));
	    }
	    if (data.description) {
	        nodes.push(p({ className: 'form-field__description' }, data.description));
	    }
	    return nodes;
	};

/***/ },
/* 91 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    i = _require.i;

	module.exports = function (name) {
	  return i({ className: 'icon icon-' + name });
	};

/***/ },
/* 92 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var c = __webpack_require__(93).get;

	var _require = __webpack_require__(96),
	    required = _require.required;

	var _require2 = __webpack_require__(78),
	    label = _require2.label,
	    span = _require2.span;

	module.exports = function (data) {
	    var isRequired = data.validations ? data.validations.indexOf(required) > -1 : false;
	    return label({
	        className: 'form-field__label',
	        for: 'ff-' + data.name
	    }, data.label || '', data.type === 'message' ? null : span({
	        className: isRequired ? 'form-field__required' : 'form-field__optional'
	    }, isRequired ? c('required') : c('optional')));
	};

/***/ },
/* 93 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var files = {};
	files.en = __webpack_require__(94).en;
	files.eo = __webpack_require__(95).eo;

	// Given a key and the language, provide the appropriate content.
	var get = function get(key) {
	    var language = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 'en';

	    if (!files[language]) {
	        return 'No Language > ' + language;
	    }
	    if (!files[language][key]) {
	        return 'Not Found > ' + language + ' @ ' + key;
	    }
	    return files[language][key];
	};

	module.exports = { get: get };

/***/ },
/* 94 */
/***/ function(module, exports) {

	module.exports = {
		"en": {
			"boolean": "Must be true or false.",
			"change_password_url": "To change your password, please visit {url}",
			"clear": "Clear",
			"datetime": "Must be a datetime.",
			"dict": "Must be a dict.",
			"email": "Must be an email.",
			"en_us": "American English",
			"en": "English",
			"entity_id": "Must be an entity ID.",
			"entity_kind": "Must be an entity kind.",
			"eo": "Esperanto",
			"error_need_correct": "At least one option must be correct.",
			"error_options": "All options must have value, correct, and feedback.",
			"es": "Spanish",
			"field": "No such field.",
			"integer": "Must be an integer.",
			"ko": "Korean",
			"language": "Must be a language.",
			"list": "Must be a list.",
			"maxlength": "Must have maximum length of {length}.",
			"minlength": "Must have minimum length of {length}.",
			"notice_create_topic": "{user_name} created a new topic, {topic_name}, for {entity_kind} {entity_name}.",
			"notice_create_proposal": "{user_name} created a new proposal, {proposal_name}, for {entity_kind} {entity_name}.",
			"notice_block_proposal": "{user_name} blocked proposal {proposal_name}, for {entity_kind} {entity_name}.",
			"notice_decline_proposal": "{user_name} declined proposal {proposal_name}, for {entity_kind}: {entity_name}.",
			"notice_accept_proposal": "Sagefy accepted proposal {proposal_name}, for {entity_kind} {entity_name}.",
			"notice_create_post": "{user_name} created a new post under topic {topic_name}, for {entity_kind} {entity_name}.",
			"notice_create_vote": "{user_name} created a new vote under topic {topic_name}, for {entity_kind} {entity_name}.",
			"notice_come_back": "It has been awhile. Come back and learn more with us!",
			"no_match": "Username and password do not match.",
			"no_options": "No options avaliable.",
			"no_topic": "Cannot find topic.",
			"no_user": "No user by that name.",
			"not_found": "Not found.",
			"number": "Must be a number.",
			"optional": "Optional.",
			"options": "Must be one of {options}.",
			"required": "Required.",
			"self_efficacy": "You are fully in control of your results. To learn faster, own your victories and mistakes.",
			"string_or_number": "Must be a string or number.",
			"string": "Must be a string.",
			"unique": "Must be unique.",
			"url": "Must be a full URL.",
			"uuid": "Must be a UUID.",
			"welcome": "Welcome to the Sagefy Service."
		}
	};

/***/ },
/* 95 */
/***/ function(module, exports) {

	module.exports = {
		"eo": {
			"required": "Postulo."
		}
	};

/***/ },
/* 96 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/*
	Validations are functions which return string if there's an issue
	or a nothing if okay.
	*/

	var util = __webpack_require__(9);
	var c = __webpack_require__(93).get;

	var isBlank = function isBlank(val) {
	    return val === null || val === undefined || util.isString(val) && val === '';
	};

	// Validation functions should return a string on error,
	// or return nothing if there is no problem.

	// Require there to be content.
	var required = function required(val) {
	    if (isBlank(val)) {
	        return c('required');
	    }
	};

	// Require the field to be an email address if value is present.
	var email = function email(val) {
	    if (!isBlank(val) && (!util.isString(val) || !val.match(/^\S+@\S+\.\S+$/))) {
	        return c('email');
	    }
	};

	// Require the field to contain a minimum length if value is present.
	var minlength = function minlength(val, len) {
	    if (!isBlank(val) && (util.isString(val) || util.isArray(val)) && val.length < len) {
	        return c('minlength').replace('{length}', len);
	    }
	};

	// Require the value to be one of defined options
	var isOneOf = function isOneOf(val) {
	    for (var _len = arguments.length, opts = Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
	        opts[_key - 1] = arguments[_key];
	    }

	    if (!isBlank(val) && opts.indexOf(val) === -1) {
	        return c('options').replace('{options}', opts.join(' '));
	    }
	};

	module.exports = { required: required, email: email, minlength: minlength, isOneOf: isOneOf };

/***/ },
/* 97 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    input = _require.input;

	module.exports = function (data) {
	    return input({
	        id: 'ff-' + data.name,
	        name: data.name,
	        placeholder: data.placeholder || '',
	        type: data.type || 'text',
	        value: data.value || data.default || '',
	        size: data.size || 40
	    });
	};

/***/ },
/* 98 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    textarea = _require.textarea;

	module.exports = function (data) {
	    return textarea({
	        id: 'ff-' + data.name,
	        name: data.name,
	        placeholder: data.placeholder || '',
	        cols: data.cols || 40,
	        rows: data.rows || 4
	    }, data.value || '');
	};

/***/ },
/* 99 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    button = _require.button;

	var icon = __webpack_require__(91);

	module.exports = function (data) {
	    return button({
	        type: 'submit',
	        disabled: data.disabled,
	        id: data.id
	    }, icon(data.icon), ' ', data.label);
	};

/***/ },
/* 100 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/*
	- name           required, what to send to the API
	- count          required, number of options to expect
	- url            default: null
	- multiple       default: false
	- inline         default: false
	- showClear      default: false
	- showOverlay    default: false 0-6, true 7+
	- showSearch     default: false 0-20 and not url, true 21+ or url
	- options:
	    either options or url are required .. [{value: '', label: ''}]
	*/

	var c = __webpack_require__(93).get;

	var _require = __webpack_require__(78),
	    ul = _require.ul;

	var optionTemplate = __webpack_require__(101);

	module.exports = function (data) {
	    if (!data.options || data.options.length === 0) {
	        return c('no_options');
	    }

	    var html = [];

	    html.push(ul({
	        className: 'form-field--select__ul' + (data.inline ? ' form-field--select__ul--inline' : '')
	    }, data.options.map(function (o) {
	        return optionTemplate({
	            name: data.name,
	            muliple: data.multiple,
	            value: o.value,
	            checked: data.value ? o.value === data.value : o.value === data.default,
	            label: o.label,
	            disabled: o.disabled
	        });
	    }))

	    // if data.showOverlay
	    //     html.push(
	    //         div({className: 'select__selected'})
	    //         // TODO-3 List options that have already been selected
	    //         div({className: 'select__overlay'})
	    //     )
	    //
	    // if data.showClear
	    //     html.push(
	    //         a(
	    //             {className: 'clear', href: '#'}
	    //             icon('remove')
	    //             c('clear')
	    //         )
	    //     )
	    //
	    // if data.showSearch
	    //     html.push(
	    //         input({type: 'search', name: 'search'})
	    //     )

	    );return html;
	};

/***/ },
/* 101 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    li = _require.li,
	    label = _require.label,
	    input = _require.input;

	module.exports = function (data) {
	    return li(label({
	        className: 'form-field--select__label' + (data.disabled ? ' form-field--select__label--disabled' : '')
	    }, input({
	        type: data.multiple ? 'checkbox' : 'radio',
	        value: data.value || '',
	        name: data.name,
	        checked: data.checked,
	        disabled: data.disabled || false
	    }), ' ', data.label));
	};

/***/ },
/* 102 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    table = _require.table,
	    thead = _require.thead,
	    tfoot = _require.tfoot,
	    tbody = _require.tbody,
	    tr = _require.tr,
	    th = _require.th,
	    td = _require.td,
	    a = _require.a;

	var _require2 = __webpack_require__(7),
	    ucfirst = _require2.ucfirst;

	var formFieldInput = __webpack_require__(97);
	var formFieldSelect = __webpack_require__(100);
	var icon = __webpack_require__(91);

	var field = function field(_ref) {
	    var name = _ref.name,
	        index = _ref.index,
	        col = _ref.col,
	        row = _ref.row,
	        lock = _ref.lock;

	    if (lock) {
	        return row[col.name];
	    }

	    if (col.type === 'select') {
	        return formFieldSelect({
	            name: name + '.' + index + '.' + col.name,
	            value: row[col.name],
	            options: col.options
	        });
	    }

	    if (col.type === 'text') {
	        return formFieldInput({
	            type: 'text',
	            size: 30,
	            name: name + '.' + index + '.' + col.name,
	            value: row[col.name]
	            // TODO-3 placeholder
	            // TODO-3 default
	        });
	    }
	};

	module.exports = function (data) {
	    /*
	    data.columns: array of field names
	    data.values: array of objects
	    data.lock [Boolean]
	    data.name
	    */

	    var value = void 0;
	    if (data.value && data.value.length) {
	        value = data.value;
	    } else {
	        value = [{}];
	    }

	    var columns = data.columns || [];

	    return table({ attributes: { 'data-name': data.name } }, thead(tr(columns.map(function (col) {
	        return th({ attributes: { 'data-col': col.name } }, ucfirst(col.name));
	    }),
	    // TODO-2 th()  // For reordering
	    th // For deleting
	    ())), tfoot(tr(td({ colSpan: columns.length + 1 }, // TODO-2 +2 reordering
	    a({ href: '#', className: 'form-field--list__add-row' }, icon('create'), ' Add Row')))), tbody(value.map(function (row, index) {
	        return tr(columns.map(function (col) {
	            return td(field({
	                name: data.name,
	                index: index,
	                col: col,
	                row: row,
	                lock: data.lock
	            }));
	        }),
	        // TODO-2 move row td(
	        //     a(
	        //         {title: 'Reorder', href: '#', className: 'move-row'}
	        //         icon('move')
	        //     )
	        // )
	        td(a({
	            title: 'Remove',
	            href: '#',
	            className: 'form-field--list__remove-row',
	            attributes: {
	                'data-index': index
	            }
	        }, icon('remove'))));
	    })));
	};

/***/ },
/* 103 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    ul = _require.ul,
	    li = _require.li,
	    a = _require.a,
	    input = _require.input;

	var icon = __webpack_require__(91);
	var previewCardHead = __webpack_require__(104);
	var previewUnitHead = __webpack_require__(107);
	var previewSubjectHead = __webpack_require__(108);

	module.exports = function (data) {
	    var entities = data.value || data.default || [];
	    return div(entities.length ? ul({ className: 'form-field--entities__ul' }, entities.map(function (entity, index) {
	        return li(a({
	            id: entity.id,
	            href: '#',
	            className: 'form-field--entities__remove'
	        }, icon('remove'), ' Remove'), entity.kind === 'card' ? previewCardHead({
	            name: entity.name,
	            kind: entity.kind
	        }) : entity.kind === 'unit' ? previewUnitHead({
	            name: entity.name,
	            body: entity.body
	        }) : entity.kind === 'subject' ? previewSubjectHead({
	            name: entity.name,
	            body: entity.body
	        }) : null, Object.keys(entity).map(function (key) {
	            return input({
	                type: 'hidden',
	                name: data.name + '.' + index + '.' + key,
	                value: entity[key]
	            });
	        }));
	    })) : null, data.add ? a({ className: 'form-field--entities__a', href: data.add.url }, icon('search'), ' ' + data.add.label) : null);
	};

/***/ },
/* 104 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    span = _require.span;

	var _require2 = __webpack_require__(7),
	    ucfirst = _require2.ucfirst;

	var icon = __webpack_require__(91);

	var _require3 = __webpack_require__(105),
	    previewName = _require3.previewName;

	module.exports = function previewCardHead(_ref) {
	    var name = _ref.name,
	        kind = _ref.kind,
	        _ref$url = _ref.url,
	        url = _ref$url === undefined ? false : _ref$url,
	        _ref$labelKind = _ref.labelKind,
	        labelKind = _ref$labelKind === undefined ? false : _ref$labelKind;

	    var cardKindLabel = kind ? span({ className: 'preview--card__kind' }, icon(kind.toLowerCase()), ucfirst(kind)) : null;
	    return div({ className: 'preview--card__head' }, previewName({
	        name: [cardKindLabel, ' ', name],
	        kind: 'card',
	        url: url,
	        labelKind: labelKind
	    }));
	};

/***/ },
/* 105 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    a = _require.a,
	    h3 = _require.h3,
	    span = _require.span,
	    ul = _require.ul,
	    li = _require.li,
	    em = _require.em,
	    h4 = _require.h4;

	var _require2 = __webpack_require__(7),
	    ucfirst = _require2.ucfirst;

	var icon = __webpack_require__(91);
	var timeago = __webpack_require__(106);
	var c = __webpack_require__(93).get;

	function hasValue(val) {
	    return typeof val !== 'undefined' && val !== null;
	}

	var shared = {
	    previewName: function previewName(_ref) {
	        var name = _ref.name,
	            kind = _ref.kind,
	            url = _ref.url,
	            labelKind = _ref.labelKind;

	        var label = labelKind ? span({ className: 'preview__kind-label' }, icon(kind), ' ', ucfirst(kind)) : icon(kind);
	        return url ? a({ href: url }, h3(label, ' ', name)) : h3(label, ' ', name);
	    },
	    previewCreated: function previewCreated(created) {
	        return created ? timeago(created, { right: true }) : null;
	    },
	    previewStatus: function previewStatus(status) {
	        return status ? span({ className: 'preview__status--' + status }, icon(status === 'accepted' ? 'good' : status === 'blocked' ? 'bad' : status === 'declined' ? 'bad' : 'progress'), ' ', ucfirst(status)) : null;
	    },
	    previewAvailable: function previewAvailable(available) {
	        return hasValue(available) ? available ? span({ className: 'preview__available' }, icon('good'), ' Available') : span({ className: 'preview__hidden' }, icon('bad'), ' Hidden') : null;
	    },
	    previewLanguage: function previewLanguage(language) {
	        return language ? span({ className: 'preview__language' }, 'Language: ', em(c(language))) : null;
	    },
	    previewCommon: function previewCommon(_ref2) {
	        var created = _ref2.created,
	            status = _ref2.status,
	            available = _ref2.available,
	            language = _ref2.language;

	        return [shared.previewCreated(created), shared.previewStatus(status), shared.previewAvailable(available), shared.previewLanguage(language)];
	    },
	    previewRequires: function previewRequires(requires) {
	        // url name id
	        return requires && requires.length ? [h4('Requires'), ul(requires.map(function (require) {
	            return li(require.url ? a({ href: require.url }, require.name || require.id) : require.name || require.id);
	        }))] : null;
	    },
	    previewTags: function previewTags(tags) {
	        return tags && tags.length ? span('Tags: ' + tags.join(', ')) : null;
	    }
	};

	module.exports = shared;

/***/ },
/* 106 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    span = _require.span;

	var _require2 = __webpack_require__(7),
	    timeAgo = _require2.timeAgo;

	module.exports = function (time) {
	    var _ref = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {},
	        right = _ref.right;

	    return span({
	        className: 'timeago' + (right ? ' timeago--right' : '')
	    }, timeAgo(time));
	};

/***/ },
/* 107 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    p = _require.p;

	var _require2 = __webpack_require__(105),
	    previewName = _require2.previewName;

	module.exports = function previewUnitHead(_ref) {
	    var name = _ref.name,
	        body = _ref.body,
	        _ref$url = _ref.url,
	        url = _ref$url === undefined ? false : _ref$url,
	        _ref$labelKind = _ref.labelKind,
	        labelKind = _ref$labelKind === undefined ? false : _ref$labelKind;

	    return div({ className: 'preview--unit__head' }, previewName({ name: name, kind: 'unit', url: url, labelKind: labelKind }), body ? p(body) : null);
	};

/***/ },
/* 108 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    p = _require.p;

	var _require2 = __webpack_require__(105),
	    previewName = _require2.previewName;

	module.exports = function previewSubjectHead(_ref) {
	    var name = _ref.name,
	        body = _ref.body,
	        _ref$url = _ref.url,
	        url = _ref$url === undefined ? false : _ref$url,
	        _ref$labelKind = _ref.labelKind,
	        labelKind = _ref$labelKind === undefined ? false : _ref$labelKind;

	    return div({ className: 'preview--subject__head' }, previewName({ name: name, kind: 'subject', url: url, labelKind: labelKind }), body ? p(body) : null);
	};

/***/ },
/* 109 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    li = _require.li;

	var icon = __webpack_require__(91);

	module.exports = function (_ref) {
	    var name = _ref.name,
	        message = _ref.message;
	    return li({ className: 'form__error' }, icon('bad'), [' ', name ? name + ': ' : '', message].join(''));
	};

/***/ },
/* 110 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(96),
	    required = _require.required,
	    email = _require.email,
	    minlength = _require.minlength,
	    isOneOf = _require.isOneOf;

	module.exports = {
	    name: {
	        type: 'text',
	        validations: [required]
	    },
	    email: {
	        type: 'email',
	        validations: [required, email]
	    },
	    password: {
	        type: 'password',
	        validations: [required, [minlength, 8]]
	    },
	    'settings.email_frequency': {
	        type: 'select',
	        multiple: false,
	        options: [{
	            value: 'immediate'
	        }, {
	            value: 'daily'
	        }, {
	            value: 'weekly'
	        }, {
	            value: 'never'
	        }],
	        validations: [required, [isOneOf, 'immediate', 'daily', 'weekly', 'never']]
	    }
	};

/***/ },
/* 111 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    p = _require.p,
	    br = _require.br,
	    a = _require.a;

	var form = __webpack_require__(89);
	var icon = __webpack_require__(91);
	var userSchema = __webpack_require__(110);

	var _require2 = __webpack_require__(9),
	    extend = _require2.extend;

	var _require3 = __webpack_require__(7),
	    createFieldsData = _require3.createFieldsData,
	    findGlobalErrors = _require3.findGlobalErrors;

	var fields = [{
	    name: 'name',
	    label: 'Name or Email',
	    placeholder: 'e.g. Unicorn'
	}, {
	    name: 'password',
	    label: 'Password',
	    placeholder: ''
	}, {
	    type: 'submit',
	    name: 'log-in',
	    label: 'Log In',
	    icon: 'log-in'
	}];

	fields.forEach(function (field, index) {
	    fields[index] = extend({}, userSchema[field.name] || {}, field);
	});

	module.exports = function (data) {
	    if (data.currentUserID) {
	        div('Logged in already.');
	    }

	    var instanceFields = createFieldsData({
	        schema: userSchema,
	        fields: fields,
	        errors: data.errors,
	        formData: data.formData,
	        sending: data.sending
	    });

	    var globalErrors = findGlobalErrors({
	        fields: fields,
	        errors: data.errors
	    });

	    return div({ id: 'log-in', className: 'page' }, h1('Log In'), p("Don't have an account? ", a({ href: '/sign_up' }, icon('sign-up'), ' Sign Up'), '.', br(), 'Forgot your password? ', a({ href: '/password' }, icon('password'), ' Reset'), '.'), form({
	        fields: instanceFields,
	        errors: globalErrors
	    }));
	};

/***/ },
/* 112 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    p = _require.p;

	var form = __webpack_require__(89);
	var userSchema = __webpack_require__(110);

	var _require2 = __webpack_require__(9),
	    extend = _require2.extend;

	var _require3 = __webpack_require__(7),
	    createFieldsData = _require3.createFieldsData,
	    findGlobalErrors = _require3.findGlobalErrors;

	var wizard = __webpack_require__(113);

	var emailFields = [{
	    name: 'email',
	    label: 'Email',
	    description: 'We need your email to send the token.',
	    placeholder: 'ex: unicorn@example.com'
	}, {
	    type: 'submit',
	    name: 'submit',
	    label: 'Send Token',
	    icon: 'create'
	}];

	emailFields.forEach(function (field, index) {
	    emailFields[index] = extend({}, userSchema[field.name] || {}, field);
	});

	var passwordFields = [{
	    name: 'password',
	    label: 'Password'
	}, {
	    type: 'submit',
	    name: 'submit',
	    label: 'Change Password',
	    icon: 'create'
	}];

	passwordFields.forEach(function (field, index) {
	    passwordFields[index] = extend({}, userSchema[field.name] || {}, field);
	});

	module.exports = function (data) {
	    // TODO-3 the state should be provided solely by data,
	    //      the view should not be looking at the window query string
	    var _data$routeQuery = data.routeQuery,
	        token = _data$routeQuery.token,
	        id = _data$routeQuery.id;

	    var state = token && id ? 'password' : data.passwordPageState || 'email';
	    return div({
	        id: 'password',
	        className: 'page ' + state
	    }, h1('Create a New Password'), wizard({
	        options: [{ name: 'email', label: 'Enter Email' }, { name: 'inbox', label: 'Check Inbox' }, { name: 'password', label: 'Change Password' }],
	        state: state
	    }), getNodesForState(state, data));
	};

	var getNodesForState = function getNodesForState(state, data) {
	    var instanceFields = void 0;
	    var globalErrors = void 0;
	    if (state === 'email') {
	        instanceFields = createFieldsData({
	            schema: userSchema,
	            fields: emailFields,
	            errors: data.errors,
	            formData: data.formData,
	            sending: data.sending
	        });
	        globalErrors = findGlobalErrors({
	            fields: emailFields,
	            errors: data.errors
	        });
	        return form({
	            fields: instanceFields,
	            errors: globalErrors
	        });
	    }
	    if (state === 'inbox') {
	        return p('Check your inbox. Be sure to check your spam folder.');
	    }
	    if (state === 'password') {
	        instanceFields = createFieldsData({
	            schema: userSchema,
	            fields: passwordFields,
	            errors: data.errors,
	            formData: data.formData,
	            sending: data.sending
	        });
	        globalErrors = findGlobalErrors({
	            fields: passwordFields,
	            errors: data.errors
	        });
	        return form({
	            fields: instanceFields,
	            errors: globalErrors
	        });
	    }
	};

/***/ },
/* 113 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    ol = _require.ol,
	    li = _require.li;

	module.exports = function (_ref) {
	    var options = _ref.options,
	        state = _ref.state;
	    return ol({ className: 'wizard' }, options.map(function (option) {
	        return li({
	            href: '#',
	            className: 'wizard__li' + (state === option.name ? ' wizard__li--selected' : '')
	        }, option.label);
	    }));
	};

/***/ },
/* 114 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	// Note: we won't translate this copy as its dev specific
	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    h2 = _require.h2,
	    p = _require.p;

	var data = __webpack_require__(115);

	module.exports = function () {
	    return div({ id: 'styleguide', className: 'page' }, h1('Style Guide & Component Library'), p('Welcome to the Sagefy Style Guide. ', 'This page covers the styling and ', 'conventions of Sagefy user interfaces. ', 'This guide also include commonly used components. ', 'Suggestions are welcome via pull requests. '), writeStyleguide());
	};

	var writeStyleguide = function writeStyleguide() {
	    var tags = [];
	    Object.keys(data).forEach(function (title) {
	        var o = data[title];
	        if (o) {
	            tags.push(h2(title), o.description ? p(o.description) : null);
	        }
	    });
	    return tags;
	};

	// TODO-2 render description markdown => vdom
	// TODO-2 render example using .tmpl file

/***/ },
/* 115 */
/***/ function(module, exports) {

	module.exports = {
		"Body Element": {
			"title": "Body Element",
			"description": "The `body` tag is centered by default, and sets up basic typographical adjustments.\n\nFor more on web typography, check out [Practical Typography](http://practicaltypography.com/).\n"
		},
		"Border Box": {
			"title": "Border Box",
			"description": "Sagefy uses the box sizing mode of border box. See the [Paul Irish article](http://www.paulirish.com/2012/box-sizing-border-box-ftw/).\n"
		},
		"Buttons": {
			"title": "Buttons",
			"description": "Buttons are one of the most recognized elements of web design. Sagefy provides buttons in a variety of styles. In most places, where there are multiple buttons, one and only one button should be emphasized."
		},
		"Clearfix": {
			"title": "Clearfix",
			"description": "Clearfix clears any floats within the element so it doesn't impact neighboring elements.\n"
		},
		"Fonts": {
			"title": "Fonts",
			"description": "Sagefy uses Georgia for titles and body copy. Sagefy avoids 'bold' because Georgia is very heavy. Sagefy uses DejaVu Sans Mono derivatives for monospaced.\n\n- **Base**: georgia, serif\n- **Monospace**: menlo, \"dejavu sans mono\", \"bitstream vera sans mono\", consolas, inconsolata, \"lucida console\", monaco, monospace\n"
		},
		"Font Sizes": {
			"title": "Font Sizes",
			"description": "Font sizes are fuzzified by names. Available sizes are:\n\n- small\n- normal\n- large\n- big\n- epic\n"
		},
		"Grid": {
			"title": "Grid",
			"description": "Any element may be set to a specific number of columns, using the placeholder `col-n`. Any element with set columns larger than the available screen will be reduced to the maximum width.\n"
		},
		"Headings, Subheadings, and Header Groups": {
			"title": "Headings, Subheadings, and Header Groups",
			"description": "All elements <code>h1</code> through <code>h6</code> are styled. Sub-headers use the class <code>subheader</code> when used directly below a higher order header. An <code>hgroup</code> collapses the margins between the headers. Optionally, elements can float along with the header. The most easy way to accomplish this is to wrap the header in an <code>hgroup</code> and add the class <code>inline-block</code> to the header tag."
		},
		"Horizontal Rules": {
			"title": "Horizontal Rules",
			"description": "Horizontal rules are avoided as Sagefy prefers whitespace over lines. Rules are useful in certain situations, however."
		},
		"iFrame": {
			"title": "iFrame",
			"description": "TBD\n"
		},
		"Images": {
			"title": "Images",
			"description": "Alt tags, title tags, and captions for images are recommended where possible. Images subscribe to the basic grid of `13px` as much as possible, more so on the width. Additionally, widths that match the grid system, `52n + 26(n-1)`, are preferable."
		},
		"Inline-level Elements": {
			"title": "Inline-level Elements",
			"description": "All normal tag operations are supported and provide expected results. Note that `b`, `s`, and `u`tags are not supported, and `i` tags are reserved for icons, not italics."
		},
		"Inputs": {
			"title": "Inputs",
			"description": "Range elements do not use sliders. Instead, ranges are input as two text fields."
		},
		"Inline Labels": {
			"title": "Inline Labels",
			"description": "Labels are available in each of the basic hues. It is typically used for numbers or to draw unique emphasis to words or short phrases."
		},
		"Links": {
			"title": "Links",
			"description": "Links are simply blue in color, and like other states, _lighten_ on hover and focus, and _darken_ on active (clicked) or selected. Icons can be optionally included in links. Links stay underlined to support the color. Visited links receive no extraordinary treatment."
		},
		"Lists": {
			"title": "Lists",
			"description": "Unordered lists follow standard conventions. Line items do not hold extra margins. Only root-level unordered lists have a bottom margin. Ordered lists follow the standard conventions as well.\n"
		},
		"Metrics": {
			"title": "Metrics",
			"description": "Sagefy uses a larger-than-typical metric system. The rhythm is 26px both vertically and horizontally. The base font size is 18px with a line-height of 26px. Columns are 52px and gutters are 26px. Because of Sagefy's large metrics, a great deal of focus and minimalism is required.\n"
		},
		"Vendor Mixins": {
			"title": "Vendor Mixins",
			"description": "Whenever a wrapped property is called, all vendor prefixes are automatically added as well.\n\nThe following properties receive vendor mixins:\n\n- border-radius\n- transition\n- animation\n- box-sizing\n- filter\n- flex-flow\n- justify-content\n- flex-basis\n- order\n"
		},
		"Monowidth Font Elements": {
			"title": "Monowidth Font Elements",
			"description": "TBD\n"
		},
		"Paragraphs": {
			"title": "Paragraphs",
			"description": "Update margin on paragraph tags to match all other block level elements.\n"
		},
		"Placeholders": {
			"title": "Placeholders",
			"description": "Placeholders provide the user with an example of the what the field should contain. Typically, include _e.g._ at the beginning. Do not use placeholder in place of labels."
		},
		"Quotes and Citations": {
			"title": "Quotes and Citations",
			"description": "The `q` and `cite` tags are used together to indicate a quote and a citation. All quotes are cited. No quote marks are included when using the `q` tag. In addition to inline quotations, blockquotes can be used to pull a quote out of inline copy. The `q` and `cite` tags are used inside the `blockquote` tag."
		},
		"Tables": {
			"title": "Tables",
			"description": "Tables are zebra-striped, and common elements such as header and footer rows are available. Rows classes are available for each hue; as they only change hue, another indicator needs to be used to differentiate row types. Supplimental tags, such as `tbody` are recommended.\n"
		},
		"Alert": {
			"title": "Alert",
			"description": "Systemic-alerts are often used when an error has occured. Alerts are fixed to the page until a user chooses to close them.\n"
		},
		"Form Fields": {
			"title": "Form Fields",
			"description": "Form fields are wrapped in a class of <code>form-field</code> and the type of the form field, such as <code>form-field--text</code>."
		},
		"Field Descriptions": {
			"title": "Field Descriptions",
			"description": "In the standard vertical layout, each form field may have a short description below the field. These descriptions are particularly useful when the user may not understand the expected input, or has reservations about why the field is necessary or beneficial. Fields typically have descriptions below the field."
		},
		"Form Feedback": {
			"title": "Form Feedback",
			"description": "Forms typically have validation messages to the right of the field."
		},
		"Form Field Label": {
			"title": "Form Field Label",
			"description": "The label may contain a <code>span</code> with either <code>optional</code> or <code>required</code> as the class and copy to indicate the field is either required or optional. More useful for forms with more than three fields or several sections."
		},
		"Icons": {
			"title": "Icons",
			"description": "Sagefy uses [FontAwesome](https://fortawesome.github.io/Font-Awesome/) where applicable. Use the `i` tag for icons, not italics. When presenting icons, label the icon. If you must choose between an icon and text, prefer text.\n"
		},
		"Menu": {
			"title": "Menu",
			"description": "Sagefy's most common navigational element is a simple menu. The user clicks on the Sagefy icon, and a pane of menu options provides the user with more functionality. This helps to prevent cognitive overload.\n"
		},
		"Menu Item": {
			"title": "Menu Item",
			"description": "TBD\n"
		},
		"Notice": {
			"title": "Notice",
			"description": "TBD\n"
		},
		"Notices": {
			"title": "Notices",
			"description": "TBD\n"
		},
		"Post": {
			"title": "Post",
			"description": "TBD"
		},
		"Spinners": {
			"title": "Spinners",
			"description": "A placeholder element to wait for things to load.\n"
		},
		"Wizard": {
			"title": "Wizard",
			"description": "TBD\n"
		}
	};

/***/ },
/* 116 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	// TODO-3 move copy to content directory
	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1;

	var terms = __webpack_require__(117);

	module.exports = function () {
	    return div({ id: 'terms', className: 'page' }, h1('Sagefy Privacy Policy & Terms of Service'), terms);
	};

/***/ },
/* 117 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable quotes, max-len */
	var _require = __webpack_require__(78),
	    h2 = _require.h2,
	    p = _require.p;

	module.exports = [h2('General Terms'), p('If you have questions about these terms, contact Sagefy at <support@sagefy.org>.'), p('By using Sagefy, you agree to these terms.'), p('If you do not agree to these terms, you must stop using Sagefy.'), p('This document is effective as of January 25, 2016.'), p('Sagefy may change this document at any time without notice.'), p('If any part of this document is invalid, that part is separable from the rest of the document and the rest of this document remains valid.'), p('If Sagefy does not enforce any part of this document, Sagefy does not waive the right to enforce any part of this document.'), p("Sagefy's software is licensed under the Apache 2.0 license. <http://www.apache.org/licenses/LICENSE-2.0>"), h2('Disclaimers'), p('SAGEFY IS PROVIDED AS-IS AND AS-AVAILABLE.'), p('SAGEFY MAKES NO WARRANTIES.'), p('SAGEFY DOES NOT OFFER WARRANTIES ON MERCHANTABILITY, FITNESS FOR A PARTICULAR USE, OR NON-INFRINGEMENT OF INTELLECTUAL PROPERTY.'), p('SAGEFY IS NOT LIABLE FOR ANY DAMAGES COMING FROM USE OF SAGEFY.'), h2('Personal Information'), p('Sagefy may contact you by your provided email address.'), p('Sagefy provides support in English, via email, but only as available.'), p('Sagefy may use cookies to keep you logged in and to personalize the service.'), p('Sagefy may collect personally identifying information to provide services.'), p('Sagefy uses third-party services to provide service.'), p('Sagefy may send personally identifying information to trusted third-parties, such as Google Analytics and UserVoice.'), p('Sagefy does not sell or rent personally identifying information to third-parties.'), p("Sagefy may share information to law enforcement without notice only     a) if required by law,     b) to defend Sagefy's rights and property, or     c) to ensure personal safety or public safety."), p('If Sagefy merges with or is acquired by another organization, data will be transferred to that organization.'), h2('User Accounts'), p('You cannot share a single account with multiple people.'), p('You cannot make or use more than one account.'), p('If you are under the age of thirteen, you must ask a parent or guardian before using Sagefy.'), p('You are completely responsible for protecting your account, passwords, and tokens.'), p('Sagefy is not liable for any damages resulting from unauthorized use of your account.'), p("Sagefy may close accounts, cancel service, and restrict access in Sagefy's own judgement, even without notice or cause."), p('If you or Sagefy closes your account, your personal information will be removed, but your contributions will remain on the service.'), h2('Community'), p('You cannot use Sagefy to spam, defame, harass, abuse, threaten, defraud, or impersonate any person or entity.'), p('You cannot use Sagefy to collect information about other users without their consent.'), p("You cannot interfere with any other user's use of Sagefy."), p('You cannot use Sagefy for any illegal purpose.'), p('You cannot use Sagefy to distribute any software intended to cause damage, such as viruses or malware.'), h2('Sharing Content'), p('By providing content to Sagefy, you agree you own the rights to the content and the legal ability to provide the content.'), p('By providing content to Sagefy, you agree Sagefy may use this content.'), p('By providing content to Sagefy, you confirm that the content is licensed under a Creative Commons license <http://creativecommons.org/> or similar license.'), p('Sagefy does not claim property rights to user-provided content.'), p('Sagefy does not monitor or take responsibility for user contributed content.'), p('Sagefy, and its content, does not offer professional, financial, legal, or medical advice.'), p('Sagefy does not warrant any user submitted content is safe, secure, truthful, accurate, error-free, correctly categorized, or socially acceptable.'), p('No compensation will be given for user-provided content.'), p('Sagefy may update and remove user-provided content, but Sagefy does not make any commitment to update or remove content.'), p('Sagefy is not responsible for content or agreements on external websites, even if Sagefy links to them.'), h2('Security'), p('You cannot interfere with security features of Sagefy.'), p('You cannot use any sort of automated means, such as bots or scrapers, to access Sagefy.'), p('You cannot bypass measures to restrict access to Sagefy.'), p('You cannot disrupt the services with excessive requests.'), p("You cannot gain or attempt to gain unauthorized access to Sagefy's non-public data or infrastructure."), h2('DMCA'), p('If your copyright, patent, or trademark has been violated, contact <support@sagefy.org>.'), p('Notices and counter-notices must meet statutory requirements imposed by the Digital Millennium Copyright Act of 1998. ')];

/***/ },
/* 118 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	// TODO-3 move copy to content directory

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    ul = _require.ul,
	    li = _require.li,
	    a = _require.a,
	    strong = _require.strong,
	    br = _require.br;

	var uvUrl = 'https://sagefy.uservoice.com/forums/233394-general';

	module.exports = function () {
	    return div({ id: 'contact', className: 'page' }, h1('Contact Sagefy'), ul(li(strong('I have a problem with content.'), br(), 'Discuss it in the site, or propose removing it.'), li(strong('I have an idea for content.'), br(), 'Discuss it in the site.'), li(strong('I have an idea for the software.'), br(), a({ href: uvUrl }, 'Add it to our feedback forum.')), li(strong('I found a bug.'), br(), a({ href: 'https://github.com/heiskr/sagefy/issues' }, 'Add to Github issues'), '. For security issues ', a({ href: 'mailto:support@sagefy.org' }, 'send us an email'), '.'), li(strong('My copyright has been violated.'), br(), a({ href: 'mailto:support@sagefy.com' }, 'Send us an email'), '.'), li(strong('I need help with my account.'), br(), a({ href: 'mailto:support@sagefy.com' }, 'Send us an email'), '.'), li(strong("I'm a media person."), br(), a({ href: 'mailto:support@sagefy.com' }, 'Send us an email'), '.')));
	};

/***/ },
/* 119 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    p = _require.p,
	    a = _require.a,
	    hr = _require.hr;

	var userSchema = __webpack_require__(110);

	var _require2 = __webpack_require__(9),
	    extend = _require2.extend;

	var _require3 = __webpack_require__(7),
	    createFieldsData = _require3.createFieldsData,
	    findGlobalErrors = _require3.findGlobalErrors;

	var form = __webpack_require__(89);
	var spinner = __webpack_require__(120);
	var icon = __webpack_require__(91);

	var fields = [{
	    name: 'id',
	    type: 'hidden'
	}, {
	    name: 'name',
	    label: 'Name',
	    placeholder: 'ex: Unicorn'
	}, {
	    name: 'email',
	    label: 'Email',
	    placeholder: 'ex: unicorn@example.com'
	}, {
	    name: 'settings.email_frequency',
	    label: 'Email Frequency',
	    options: [{
	        label: 'Immediate'
	    }, {
	        label: 'Daily'
	    }, {
	        label: 'Weekly'
	    }, {
	        label: 'Never'
	    }],
	    inline: true
	}, {
	    name: 'submit',
	    type: 'submit',
	    label: 'Update',
	    icon: 'update'
	}];

	fields.forEach(function (field, index) {
	    fields[index] = extend({}, userSchema[field.name] || {}, field);
	});

	module.exports = function (data) {
	    var user = data.users && data.users[data.currentUserID];
	    if (!user) {
	        return spinner();
	    }

	    var instanceFields = createFieldsData({
	        schema: userSchema,
	        fields: fields,
	        errors: data.errors,
	        formData: extend({}, {
	            id: user.id,
	            name: user.name,
	            email: user.email,
	            'settings.email_frequency': user.settings.email_frequency
	        }, data.formData),
	        sending: data.sending
	    });

	    var globalErrors = findGlobalErrors({
	        fields: fields,
	        errors: data.errors
	    });

	    return div({ id: 'settings', className: 'page' }, h1('Settings'), form({
	        fields: instanceFields,
	        errors: globalErrors
	    }), hr(), p(a({ href: '/password' }, icon('password'), ' Change my password.')), p(a({ href: 'https://gravatar.com' }, icon('update'), ' Update my avatar on Gravatar.')));
	};

/***/ },
/* 120 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div;

	module.exports = function () {
	  return div({ className: 'spinner' });
	};

/***/ },
/* 121 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    p = _require.p,
	    a = _require.a;

	var notices = __webpack_require__(122);
	var spinner = __webpack_require__(120);
	var icon = __webpack_require__(91);

	module.exports = function (data) {
	    // TODO-2 update this to use a status field
	    if (!data.notices) {
	        return spinner();
	    }

	    return div({ id: 'notices', className: 'page' }, h1('Notices'), p(a({ href: '/follows' }, icon('follow'), ' Manage what I follow')), notices(data.notices));
	};

/***/ },
/* 122 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    ul = _require.ul,
	    p = _require.p;

	var notice = __webpack_require__(123);

	module.exports = function (data) {
	    if (!data.length) {
	        return p('No notices.');
	    }
	    return ul({ className: 'notices' }, data.map(function (n) {
	        return notice(n);
	    })
	    // TODO-2 request more notices
	    );
	};

/***/ },
/* 123 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    li = _require.li,
	    span = _require.span;

	var timeAgo = __webpack_require__(7).timeAgo;

	// TODO-2 add a link around the notice, and go to the appropriate page on click.

	module.exports = function (data) {
	    return li({
	        className: data.read ? 'notice' : 'notice notice--unread',
	        id: data.id
	    }, span({ className: 'notice__when' }, timeAgo(data.created)), data.body);
	};

/***/ },
/* 124 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable no-underscore-dangle */
	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    form = _require.form,
	    input = _require.input,
	    button = _require.button,
	    img = _require.img,
	    ul = _require.ul,
	    li = _require.li,
	    a = _require.a,
	    p = _require.p,
	    h3 = _require.h3,
	    span = _require.span,
	    br = _require.br;

	var spinner = __webpack_require__(120);
	var timeago = __webpack_require__(106);
	var icon = __webpack_require__(91);
	var previewSubjectHead = __webpack_require__(108);
	var previewUnitHead = __webpack_require__(107);
	var previewCardHead = __webpack_require__(104);

	var _require2 = __webpack_require__(7

	// TODO-2 when receiving ?kind={kind}, then search using that as well.

	),
	    ucfirst = _require2.ucfirst;

	module.exports = function (data) {
	    var loading = data.searchQuery && !data.searchResults;
	    var asLearner = data.route.indexOf('as_learner') > -1;

	    var inputOpts = {
	        type: 'text',
	        placeholder: 'Search',
	        name: 'search',
	        size: 40
	    };

	    inputOpts.value = data.searchQuery || null;

	    return div({ id: 'search', className: 'page' }, h1('Search'),
	    // TODO-2 add search filtering / ordering
	    form({ className: 'form--horizontal' }, div({ className: 'form-field form-field--search' }, input(inputOpts)), button({ type: 'submit' }, icon('search'), ' Search')), loading ? spinner() : null, data.searchResults && data.searchResults.length ? ul(data.searchResults.map(function (result) {
	        return li(r[result._type + 'Result'](result, asLearner));
	    })) : null, data.searchResults && data.searchResults.length === 0 ? p('No results found.') : null

	    // TODO-2 pagination
	    );
	};

	var r = {};

	r.userResult = function (result) {
	    return h3(span({ className: 'search__label' }, icon('user'), ' User'), ' ', a({ href: '/users/' + result._source.id }, img({ className: 'avatar', src: result._source.avatar }), ' ', result._source.name));
	};

	r.topicResult = function (result) {
	    return [timeago(result._source.created, { right: true }), h3(span({ className: 'search__label' }, icon('topic'), ' Topic'), ' ', a({ href: '/topics/' + result._source.id }, result._source.name)), result._source.entity.name ? a({
	        href: '/' + result._source.entity.kind + '/' + result._source.entity.id
	    }, result._source.entity.name) : null];
	};

	r.postResult = function (result) {
	    var href = '/topics/' + result._source.topic_id + '#' + result._source.id;
	    return [timeago(result._source.created, { right: true }), h3(span({ className: 'search__label' }, icon('post'), ' ', ucfirst(result._source.kind)), ' by ', a({ href: '/users/' + result._source.user.id }, result._source.user.name)), ' in topic: ', result._source.topic ? a({ href: '/topics/' + result._source.topic.id }, result._source.topic.name) : null, br(), result._source.body, ' ', a({ href: href }, 'To Post ', icon('next'))];
	};

	r.cardResult = function (result) {
	    return previewCardHead({
	        url: '/cards/' + result._source.entity_id,
	        name: result._source.name,
	        kind: result._source.kind,
	        labelKind: true
	        // TODO-3 unit name   result._source.unit_id > ???
	        // TODO-3 contents    ???
	    });
	};

	r.unitResult = function (result) {
	    return previewUnitHead({
	        url: '/units/' + result._source.entity_id,
	        name: result._source.name,
	        body: result._source.body,
	        labelKind: true
	    });
	};

	r.subjectResult = function (result) {
	    var asLearner = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;
	    return [asLearner ? a(
	    // TODO-2 if already in subjects, don't show this button
	    {
	        id: result._source.entity_id,
	        href: '#',
	        className: 'add-to-my-subjects'
	    }, icon('create'), ' Add to My Subjects') : null, previewSubjectHead({
	        url: '/subjects/' + result._source.entity_id,
	        name: result._source.name,
	        body: result._source.body,
	        labelKind: true
	    }), asLearner ? ' ' : null, asLearner ? a({
	        href: '/subjects/' + result._source.entity_id + '/tree',
	        className: 'view-units'
	    }, icon('unit'), ' View Units') : null];
	};

/***/ },
/* 125 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1;

	var _require2 = __webpack_require__(9),
	    extend = _require2.extend;

	var subjectSchema = __webpack_require__(126);
	var form = __webpack_require__(89);

	var _require3 = __webpack_require__(7),
	    createFieldsData = _require3.createFieldsData,
	    findGlobalErrors = _require3.findGlobalErrors;

	var fields = [{
	    label: 'Subject Name',
	    name: 'name'
	}, {
	    label: 'Subject Language',
	    name: 'language',
	    options: [{ label: 'English' }],
	    value: 'en'
	}, {
	    label: 'Subject Goal',
	    description: 'Start with a verb, such as: Compute the value of ' + 'dividing two whole numbers.',
	    name: 'body'
	}, {
	    name: 'members',
	    label: 'Subject Members',
	    description: 'Choose a list of units and subjects. ' + 'Cycles are not allowed.',
	    add: {
	        label: 'Add an Existing Unit or Subject',
	        url: '#'
	    }
	}, {
	    type: 'submit',
	    name: 'submit',
	    label: 'Create Subject',
	    icon: 'create'
	}];

	fields.forEach(function (field, index) {
	    fields[index] = extend({}, subjectSchema[field.name] || {}, field);
	});

	module.exports = function createSubjectCreate(data) {
	    var instanceFields = createFieldsData({
	        schema: subjectSchema,
	        fields: fields,
	        errors: data.errors,
	        formData: data.create.subject || {},
	        sending: data.sending
	    });

	    var globalErrors = findGlobalErrors({
	        fields: fields,
	        errors: data.errors
	    });

	    return div({ id: 'create', className: 'page create--subject-create' }, h1('Create a New Subject'), form({
	        fields: instanceFields,
	        errors: globalErrors
	    }));
	};

/***/ },
/* 126 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(96),
	    required = _require.required;

	module.exports = {
	    language: {
	        type: 'select',
	        validations: [required],
	        options: [{ value: 'en' }]
	    },
	    name: {
	        type: 'text',
	        validations: [required]
	    },
	    body: {
	        type: 'textarea',
	        validations: [required]
	    },
	    tags: {
	        type: 'list',
	        validations: [],
	        columns: [{ name: 'tag', type: 'text' }]
	    },
	    members: {
	        type: 'entities',
	        validations: []
	        /*
	            kind: (unit|subject)
	            id
	        */
	    }
	};

/***/ },
/* 127 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable no-underscore-dangle */

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    form = _require.form,
	    input = _require.input,
	    button = _require.button,
	    a = _require.a,
	    ul = _require.ul,
	    li = _require.li,
	    p = _require.p;

	var icon = __webpack_require__(91);
	var previewUnitHead = __webpack_require__(107);
	var previewSubjectHead = __webpack_require__(108);

	module.exports = function createSubjectAdd(data) {
	    var searchResults = data.searchResults;

	    var inputOpts = {
	        type: 'text',
	        placeholder: 'Search Unit and Subjects',
	        name: 'search',
	        size: 40
	    };
	    inputOpts.value = data.searchQuery || null;

	    return div({ id: 'create', className: 'page create--subject-add' }, h1('Add an Existing Unit or Subject to New Subject'), a({ href: '/create/subject/create' }, icon('back'), ' Back to Create Subject form'), form({ className: 'form--horizontal create--subject-add__form' }, div({ className: 'form-field form-field--search' }, input(inputOpts)), button({ type: 'submit', className: 'create--subject-add__search' }, icon('search'), ' Search')), searchResults && searchResults.length ? ul({ className: 'create--subject-add__results' }, searchResults.map(function (result) {
	        return li(a({
	            href: '/create/subject/create',
	            className: 'create--subject-add__add',
	            dataset: {
	                kind: result._type,
	                id: result._id,
	                name: result._source.name,
	                body: result._source.body
	            }
	        }, icon('create'), ' Add to Subject'), result._type === 'subject' ? previewSubjectHead({
	            name: result._source.name,
	            body: result._source.body
	        }) : result._type === 'unit' ? previewUnitHead({
	            name: result._source.name,
	            body: result._source.body
	        }) : null);
	    })) : p('No results.'));
	};

/***/ },
/* 128 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable no-underscore-dangle */
	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    h2 = _require.h2,
	    p = _require.p,
	    ul = _require.ul,
	    li = _require.li,
	    a = _require.a,
	    form = _require.form,
	    input = _require.input,
	    button = _require.button;

	var _require2 = __webpack_require__(129),
	    unitWizard = _require2.unitWizard;

	var previewSubjectHead = __webpack_require__(108);
	var icon = __webpack_require__(91);

	module.exports = function createUnitFind(data) {
	    var searchResults = data.searchResults;
	    var myRecentSubjects = data.create.myRecentSubjects;


	    var inputOpts = {
	        type: 'text',
	        placeholder: 'Search Subjects',
	        name: 'search',
	        size: 40
	    };
	    inputOpts.value = data.searchQuery || null;

	    return div({ id: 'create', className: 'page create--unit-find' }, h1('Find a Subject to Add Units'), unitWizard('find'), myRecentSubjects && myRecentSubjects.length ? div(h2('My Recent Subjects'), ul({ className: 'create--unit-find__my-recents' }, myRecentSubjects.map(function (subject) {
	        return li(a({
	            href: '/create/unit/list?' + subject.entity_id,
	            className: 'create--unit-find__choose',
	            dataset: {
	                id: subject.entity_id,
	                name: subject.name
	            }
	        }, icon('create'), ' Choose This Subject'), previewSubjectHead({
	            name: subject.name,
	            body: subject.body
	        }));
	    })), p({ className: 'create--unit-find__or' }, 'or')) : null, h2('Search for a Subject'), form({ className: 'form--horizontal create--unit-find__form' }, div({ className: 'form-field form-field--search' }, input(inputOpts)), button({ type: 'submit', className: 'create--unit-find__search' }, icon('search'), ' Search')), searchResults && searchResults.length ? ul({ className: 'create--unit-find__results' }, searchResults.map(function (result) {
	        return li(a({
	            href: '/create/unit/list?' + result._id,
	            className: 'create--unit-find__choose',
	            dataset: {
	                id: result._id,
	                name: result._source.name
	            }
	        }, icon('create'), ' Choose This Subject'), previewSubjectHead({
	            name: result._source.name,
	            body: result._source.body
	        }));
	    })) : p('No results.'), a({
	        href: '/create',
	        className: 'create__home'
	    }, icon('back'), ' Return to Create Overview'));
	};

/***/ },
/* 129 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var wizard = __webpack_require__(113);

	module.exports = {
	    unitWizard: function unitWizard() {
	        var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'find';

	        return wizard({
	            options: [{
	                label: 'Find Subject',
	                name: 'find'
	            }, {
	                label: 'Add Units',
	                name: 'list'
	            }, {
	                label: 'View',
	                name: 'view'
	            }],
	            state: state
	        });
	    },
	    cardWizard: function cardWizard() {
	        var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'find';

	        return wizard({
	            options: [{
	                label: 'Find Unit',
	                name: 'find'
	            }, {
	                label: 'Add Cards',
	                name: 'list'
	            }, {
	                label: 'View',
	                name: 'view'
	            }],
	            state: state
	        });
	    }
	};

/***/ },
/* 130 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    h3 = _require.h3,
	    a = _require.a,
	    p = _require.p,
	    hr = _require.hr,
	    ul = _require.ul,
	    li = _require.li;

	var _require2 = __webpack_require__(129),
	    unitWizard = _require2.unitWizard;

	var icon = __webpack_require__(91);
	var previewUnitHead = __webpack_require__(107);

	module.exports = function createUnitList(data) {
	    var units = data.create.units;

	    var selectedSubject = data.create.selectedSubject || {};
	    var subjectName = selectedSubject.name || '???';

	    return div({ id: 'create', className: 'page create--unit-list' }, h1('Add Units to Subject'), unitWizard('list'), h3('The following units will be added to ' + subjectName), p('We won\'t save the new/added units until you "Submit These Units".'),
	    // TODO List of existing units (if any)

	    units && units.length ? ul({ className: 'create--unit-list__units' }, units.map(function (unit, index) {
	        return li(a({
	            dataset: { index: index },
	            href: '#',
	            className: 'create--unit-list__remove'
	        }, icon('remove'), ' Remove'), previewUnitHead({
	            name: unit.name,
	            body: unit.body
	        }));
	    })) : p('No units added yet.'), a({
	        className: 'create--unit-list__create',
	        href: '/create/unit/create'
	    }, icon('create'), ' Create a New Unit'), a({
	        className: 'create--unit-list__add',
	        href: '/create/unit/add'
	    }, icon('search'), ' Add an Existing Unit'), hr(), a({
	        href: '#',
	        className: 'create--unit-list__submit'
	    }, icon('create'), ' Submit These Units'), a({
	        href: '/create',
	        className: 'create__home'
	    }, icon('back'), ' Return to Create Overview'));
	};

/***/ },
/* 131 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable no-underscore-dangle */
	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    a = _require.a,
	    form = _require.form,
	    button = _require.button,
	    input = _require.input,
	    ul = _require.ul,
	    li = _require.li,
	    p = _require.p;

	var _require2 = __webpack_require__(129),
	    unitWizard = _require2.unitWizard;

	var icon = __webpack_require__(91);
	var previewUnitHead = __webpack_require__(107);

	module.exports = function createUnitAdd(data) {
	    var searchResults = data.searchResults;

	    var inputOpts = {
	        type: 'text',
	        placeholder: 'Search Units',
	        name: 'search',
	        size: 40
	    };
	    inputOpts.value = data.searchQuery || null;

	    return div({ id: 'create', className: 'page' }, h1('Add an Existing Unit to Subject'), unitWizard('list'), a({ href: '/create/unit/list' }, icon('back'), ' Back to List of Units'), form({ className: 'form--horizontal create--unit-add__form' }, div({ className: 'form-field form-field--search' }, input(inputOpts)), button({ type: 'submit', className: 'create--unit-add__search' }, icon('search'), ' Search')), searchResults && searchResults.length ? ul({ className: 'create--unit-add__results' }, searchResults.map(function (result) {
	        return li(a({
	            href: '/create/unit/list',
	            className: 'create--unit-add__add',
	            dataset: {
	                kind: result._type,
	                id: result._id,
	                version: result._source.id,
	                name: result._source.name,
	                body: result._source.body
	            }
	        }, icon('create'), ' Add to Subject'), previewUnitHead({
	            name: result._source.name,
	            body: result._source.body
	        }));
	    })) : p('No results.'));
	};

/***/ },
/* 132 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable no-underscore-dangle */

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    form = _require.form,
	    input = _require.input,
	    button = _require.button,
	    a = _require.a,
	    ul = _require.ul,
	    li = _require.li,
	    p = _require.p;

	var icon = __webpack_require__(91);
	var previewUnitHead = __webpack_require__(107);

	module.exports = function createSubjectAdd(data) {
	    var searchResults = data.searchResults;

	    var inputOpts = {
	        type: 'text',
	        placeholder: 'Search Units',
	        name: 'search',
	        size: 40
	    };
	    inputOpts.value = data.searchQuery || null;

	    return div({ id: 'create', className: 'page create--unit-create-add' }, h1('Find Requires for New Unit'), a({ href: '/create/unit/create' }, icon('back'), ' Back to Create Unit form'), form({ className: 'form--horizontal create--unit-create-add__form' }, div({ className: 'form-field form-field--search' }, input(inputOpts)), button({
	        type: 'submit',
	        className: 'create--unit-create-add__search'
	    }, icon('search'), ' Search')), searchResults && searchResults.length ? ul({ className: 'create--unit-create-add__results' }, searchResults.map(function (result) {
	        return li(a({
	            href: '/create/unit/create',
	            className: 'create--unit-create-add__add',
	            dataset: {
	                id: result._id,
	                name: result._source.name,
	                body: result._source.body
	            }
	        }, icon('create'), ' Require this Unit'), previewUnitHead({
	            name: result._source.name,
	            body: result._source.body
	        }));
	    })) : p('No results.'));
	};

/***/ },
/* 133 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    p = _require.p,
	    a = _require.a;

	var _require2 = __webpack_require__(129),
	    unitWizard = _require2.unitWizard;

	var _require3 = __webpack_require__(9),
	    extend = _require3.extend;

	var unitSchema = __webpack_require__(134);
	var form = __webpack_require__(89);

	var _require4 = __webpack_require__(7),
	    createFieldsData = _require4.createFieldsData,
	    findGlobalErrors = _require4.findGlobalErrors;

	var icon = __webpack_require__(91);

	var fields = [{
	    label: 'Unit Name',
	    name: 'name'
	}, {
	    label: 'Unit Language',
	    name: 'language',
	    options: [{ label: 'English' }],
	    value: 'en'
	}, {
	    label: 'Unit Goal',
	    description: 'Start with a verb, such as: "Compute the value of ' + 'dividing two whole numbers."',
	    name: 'body'
	}, {
	    name: 'require_ids',
	    label: 'Unit Requires',
	    description: 'List the units required before this unit.',
	    add: {
	        url: '#',
	        label: 'Find a Unit to Require'
	    }
	}, {
	    type: 'submit',
	    name: 'submit',
	    label: 'Create Unit',
	    icon: 'create'
	}];

	fields.forEach(function (field, index) {
	    fields[index] = extend({}, unitSchema[field.name] || {}, field);
	});

	module.exports = function createUnitCreate(data) {
	    var proposedUnit = data.create && data.create.proposedUnit || {};

	    var instanceFields = createFieldsData({
	        schema: unitSchema,
	        fields: fields,
	        errors: data.errors,
	        formData: proposedUnit,
	        sending: data.sending
	    });

	    var globalErrors = findGlobalErrors({
	        fields: fields,
	        errors: data.errors
	    });

	    return div({ id: 'create', className: 'page create--unit-create' }, h1('Create a New Unit for Subject'), unitWizard('list'), form({
	        fields: instanceFields,
	        errors: globalErrors
	    }), p('After you submit here, "Submit These Units" on the list page to finish.'), a({ href: '/create/unit/list' }, icon('back'), ' Cancel & Back to List of Units'));
	};

/***/ },
/* 134 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(96),
	    required = _require.required;

	module.exports = {
	    language: {
	        type: 'select',
	        validations: [required],
	        options: [{ value: 'en' }]
	    },
	    name: {
	        type: 'text',
	        validations: [required]
	    },
	    body: {
	        type: 'textarea',
	        validations: [required]
	    },
	    tags: {
	        type: 'list',
	        validations: [],
	        columns: [{ name: 'tag', type: 'text' }]
	    },
	    require_ids: {
	        type: 'entities',
	        validations: []
	    }
	};

/***/ },
/* 135 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable no-underscore-dangle */
	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    h2 = _require.h2,
	    p = _require.p,
	    ul = _require.ul,
	    li = _require.li,
	    a = _require.a,
	    form = _require.form,
	    input = _require.input,
	    button = _require.button;

	var _require2 = __webpack_require__(129),
	    cardWizard = _require2.cardWizard;

	var previewUnitHead = __webpack_require__(107);
	var icon = __webpack_require__(91);

	module.exports = function createCardFind(data) {
	    var searchResults = data.searchResults;
	    var myRecentUnits = data.create.myRecentUnits;


	    var inputOpts = {
	        type: 'text',
	        placeholder: 'Search Units',
	        name: 'search',
	        size: 40
	    };
	    inputOpts.value = data.searchQuery || null;

	    return div({ id: 'create', className: 'page create--card-find' }, h1('Find a Unit to Add Cards'), cardWizard('find'), myRecentUnits && myRecentUnits.length ? div(h2('My Recent Units'), ul({ className: 'create--card-find__my-recents' }, myRecentUnits.map(function (unit) {
	        return li(a({
	            href: '/create/card/list?' + unit.entity_id,
	            className: 'create--card-find__choose',
	            dataset: {
	                id: unit.entity_id,
	                name: unit.name
	            }
	        }, icon('create'), ' Choose This Unit'), previewUnitHead({
	            name: unit.name,
	            body: unit.body
	        }));
	    })), p({ className: 'create--card-find__or' }, 'or')) : null, h2('Search for a Unit'), form({ className: 'form--horizontal create--card-find__form' }, div({ className: 'form-field form-field--search' }, input(inputOpts)), button({ type: 'submit', className: 'create--card-find__search' }, icon('search'), ' Search')), searchResults && searchResults.length ? ul({ className: 'create--card-find__results' }, searchResults.map(function (result) {
	        return li(a({
	            href: '/create/card/list?' + result._id,
	            className: 'create--card-find__choose',
	            dataset: {
	                id: result._id,
	                name: result._source.name
	            }
	        }, icon('create'), ' Choose This Unit'), previewUnitHead({
	            name: result._source.name,
	            body: result._source.body
	        }));
	    })) : p('No results.'), a({
	        href: '/create',
	        className: 'create__home'
	    }, icon('back'), ' Return to Create Overview'));
	};

/***/ },
/* 136 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    h3 = _require.h3,
	    a = _require.a,
	    p = _require.p,
	    hr = _require.hr,
	    ul = _require.ul,
	    li = _require.li;

	var _require2 = __webpack_require__(129),
	    cardWizard = _require2.cardWizard;

	var icon = __webpack_require__(91);
	var previewCardHead = __webpack_require__(104);

	module.exports = function createCardList(data) {
	    var cards = data.create.cards;

	    var selectedUnit = data.create.selectedUnit || {};
	    var unitName = selectedUnit.name || '???';

	    return div({ id: 'create', className: 'page create--card-list' }, h1('Add Cards to Unit'), cardWizard('list'), h3('The following cards will be added to ' + unitName), p('We won\'t save the new cards until you "Submit These Cards".'),
	    // TODO List of existing units (if any)

	    cards && cards.length ? ul({ className: 'create--card-list__cards' }, cards.map(function (card, index) {
	        return li(a({
	            dataset: { index: index },
	            href: '#',
	            className: 'create--card-list__remove'
	        }, icon('remove'), ' Remove'), previewCardHead({
	            name: card.name,
	            kind: card.kind
	        }));
	    })) : p('No cards added yet.'), a({
	        className: 'create--card-list__create',
	        href: '/create/card/create'
	    }, icon('create'), ' Create a New Card'), hr(), a({
	        href: '#',
	        className: 'create--card-list__submit'
	    }, icon('create'), ' Submit These Cards'), a({
	        href: '/create',
	        className: 'create__home'
	    }, icon('back'), ' Return to Create Overview'));
	};

/***/ },
/* 137 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    a = _require.a,
	    p = _require.p;

	var _require2 = __webpack_require__(129),
	    cardWizard = _require2.cardWizard;

	var _require3 = __webpack_require__(9),
	    extend = _require3.extend;

	var cardSchema = __webpack_require__(138);
	var videoCardSchema = __webpack_require__(139);
	var choiceCardSchema = __webpack_require__(140);
	var form = __webpack_require__(89);

	var _require4 = __webpack_require__(7),
	    createFieldsData = _require4.createFieldsData,
	    findGlobalErrors = _require4.findGlobalErrors;

	var icon = __webpack_require__(91);

	var allKindsFields = [{
	    label: 'Card Name',
	    name: 'name'
	}, {
	    label: 'Card Language',
	    name: 'language',
	    options: [{ label: 'English' }],
	    value: 'en'
	}, {
	    label: 'Card Kind',
	    name: 'kind',
	    options: [{ label: 'Video' }, { label: 'Choice' }],
	    inline: true
	}];

	/* {
	   name: 'require_ids',
	   label: 'Card Requires',
	   description: 'List the cards required before this card.',
	}, */

	var videoFields = allKindsFields.concat([{
	    label: 'Video Site',
	    name: 'data.site',
	    options: [{ label: 'YouTube' }, { label: 'Vimeo' }]
	}, {
	    label: 'Video ID',
	    name: 'data.video_id',
	    description: 'You can find the video ID in the URL. Look for https://www.youtube.com/watch?v=VIDEO_ID_HERE'
	}, {
	    type: 'submit',
	    name: 'submit',
	    label: 'Create Video Card',
	    icon: 'create'
	}]);

	var choiceFields = allKindsFields.concat([{
	    label: 'Question or Prompt',
	    name: 'data.body'
	}, {
	    label: 'Response Options',
	    name: 'data.options',
	    columns: [{
	        options: [{ label: 'Yes' }, { label: 'No' }]
	    }, {}, {}]
	}, {
	    label: 'Order',
	    name: 'data.order',
	    options: [{ label: 'Random' }, { label: 'Set' }]
	}, {
	    label: 'Max Options to Show',
	    name: 'data.max_options_to_show'
	}, {
	    type: 'submit',
	    name: 'submit',
	    label: 'Create Choice Card',
	    icon: 'create'
	}]);

	allKindsFields.forEach(function (field, index) {
	    allKindsFields[index] = extend({}, allKindsFields[field.name] || {}, field);
	});

	videoFields.forEach(function (field, index) {
	    videoFields[index] = extend({}, videoFields[field.name] || {}, field);
	});

	choiceFields.forEach(function (field, index) {
	    choiceFields[index] = extend({}, choiceFields[field.name] || {}, field);
	});

	module.exports = function createCardCreate(data) {
	    var proposedCard = data.create && data.create.proposedCard || {};
	    var cardKind = proposedCard.kind;

	    var fields = cardKind === 'video' ? videoFields : cardKind === 'choice' ? choiceFields : allKindsFields;

	    var schema = cardKind === 'video' ? videoCardSchema : cardKind === 'choice' ? choiceCardSchema : cardSchema;

	    var instanceFields = createFieldsData({
	        schema: schema,
	        fields: fields,
	        errors: data.errors,
	        formData: proposedCard,
	        sending: data.sending
	    });

	    var globalErrors = findGlobalErrors({
	        fields: fields,
	        errors: data.errors
	    });

	    return div({ id: 'create', className: 'page create--card-create' }, h1('Create a New Card for Unit'), cardWizard('list'), form({
	        fields: instanceFields,
	        errors: globalErrors
	    }), p('After you submit here, "Submit These Cards" on the list page to finish.'), a({ href: '/create/card/list' }, icon('back'), ' Cancel & Back to List of Cards'));
	};

/***/ },
/* 138 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(96),
	    required = _require.required;

	module.exports = {
	    language: {
	        type: 'select',
	        validations: [required],
	        options: [{ value: 'en' }]
	    },
	    unit_id: {
	        type: 'text',
	        validations: [required]
	    },
	    name: {
	        type: 'text',
	        validations: [required]
	    },
	    tags: {
	        type: 'list',
	        validations: [],
	        columns: [{ name: 'tag', type: 'text' }]
	    },
	    require_ids: {
	        type: 'entities',
	        validations: []
	    },
	    kind: {
	        type: 'select',
	        validations: [required],
	        options: [{ value: 'video' }, { value: 'choice' }]
	    }
	};

/***/ },
/* 139 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(96),
	    required = _require.required;

	var _require2 = __webpack_require__(9),
	    extend = _require2.extend;

	var cardSchema = __webpack_require__(138);

	module.exports = extend({}, cardSchema, {
	    'data.video_id': {
	        type: 'text',
	        validations: [required]
	    },
	    'data.site': {
	        type: 'select',
	        validations: [required],
	        options: [{ value: 'youtube' }, { value: 'vimeo' }]
	    }
	});

/***/ },
/* 140 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(96),
	    required = _require.required;

	var _require2 = __webpack_require__(9),
	    extend = _require2.extend;

	var cardSchema = __webpack_require__(138);

	module.exports = extend({}, cardSchema, {
	    'data.body': {
	        type: 'textarea',
	        validations: [required]
	    },
	    'data.options': {
	        type: 'list',
	        validations: [required],
	        columns: [{
	            name: 'correct',
	            type: 'select',
	            options: [{ value: 'true' }, { value: 'false' }]
	        }, { name: 'value', type: 'text' }, { name: 'feedback', type: 'text' }]
	    },
	    'data.order': {
	        type: 'select',
	        validations: [required],
	        options: [{ value: 'random' }, { value: 'set' }],
	        default: 'random'
	    },
	    'data.max_options_to_show': {
	        type: 'number',
	        validations: [required],
	        default: 4
	    }
	});

/***/ },
/* 141 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    p = _require.p,
	    a = _require.a,
	    ul = _require.ul,
	    li = _require.li,
	    small = _require.small;

	var info = __webpack_require__(142);
	var icon = __webpack_require__(91);

	module.exports = function () {
	    return div({ id: 'create', className: 'page' }, h1('Create Cards, Units, and Subjects'), ul({ className: 'create__options' }, li(a({
	        className: 'create__route ',
	        href: '/create/subject/create'
	    }, icon('subject'), ' Create a Subject'), ' Start here. ', small(' (You can add existing units and ', 'subjects to the new subject.)')), li(a({ className: 'create__route', href: '/create/unit/find' }, icon('unit'), ' Add Units'), ' to an existing subject.'), li(a({ className: 'create__route', href: '/create/card/find' }, icon('card'), ' Add Cards'), ' to an existing unit.')), info(), p('Do you want to change an existing card, unit, or subject? ', a({ href: '/search' }, icon('search'), ' Search for it, then click edit'), '.'));
	};

/***/ },
/* 142 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h3 = _require.h3,
	    ul = _require.ul,
	    li = _require.li,
	    strong = _require.strong,
	    br = _require.br,
	    small = _require.small,
	    p = _require.p,
	    a = _require.a;

	var icon = __webpack_require__(91);

	module.exports = function () {
	    return div({ className: 'entity-info' }, h3('What are cards, units, and subjects?'), ul(li('A ', icon('card'), ' ', strong('card'), ' is a single learning activity.', br(), small('(Examples: a 3-minute video or a multiple choice question.)')), li('A ', icon('unit'), ' ', strong('unit'), ' is a single learning goal.', br(), small('(Example: "What is mean, median, and mode?")')), li('A ', icon('subject'), ' ', strong('subject'), ' is a collection of units and other subjects.', br(), small('(Like a course, but at any scale. ', 'Such as "Measures of Central Tendency", "Intro to Statistics", ', 'or even a full degree program.)'))), p('For more details and examples, ', a({ href: 'https://youtu.be/gFn4Q9tx7Qs' }, 'check out this 3-minute overview video'), '.'));
	};

/***/ },
/* 143 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    p = _require.p,
	    strong = _require.strong;

	var form = __webpack_require__(89);
	var getPostFields = __webpack_require__(144).getFields;
	var getPostSchema = __webpack_require__(144).getSchema;

	var _require2 = __webpack_require__(7),
	    createFieldsData = _require2.createFieldsData,
	    prefixObjectKeys = _require2.prefixObjectKeys,
	    ucfirst = _require2.ucfirst,
	    findGlobalErrors = _require2.findGlobalErrors;

	var _require3 = __webpack_require__(9),
	    extend = _require3.extend;

	var topicSchema = __webpack_require__(148);
	var spinner = __webpack_require__(120);

	var classes = function classes(formData) {
	    var topicID = formData['topic.id'];
	    var postKind = formData['post.kind'];
	    var entityKind = formData['post.entity_version.kind'];
	    var cardKind = formData['entity.kind'];
	    return ['page', topicID ? 'update' : 'create', postKind ? 'post-' + postKind : '', entityKind ? 'entity-' + entityKind : '', cardKind ? 'card-' + cardKind : ''].join(' ');
	};

	var getFields = function getFields(formData) {
	    var fields = [];
	    if (formData['topic.id']) {
	        fields.push({
	            name: 'topic.id'
	        });
	    }
	    fields = fields.concat([{
	        name: 'topic.entity_id'
	    }, {
	        name: 'topic.entity_kind'
	    }, {
	        name: 'topic.name',
	        label: 'Topic Name'
	    }]);
	    return fields;
	};

	var getTopicID = function getTopicID(data) {
	    var match = data.route.match(/^\/topics\/([\d\w\-_]+)\/update$/);
	    if (match) {
	        return match[1];
	    }
	    return null;
	};

	var getEntityByKind = function getEntityByKind(data, kind, id) {
	    if (kind === 'card') {
	        return data.cards && data.cards[id];
	    }
	    if (kind === 'unit') {
	        return data.units && data.units[id];
	    }
	    if (kind === 'subject') {
	        return data.subjects && data.subjects[id];
	    }
	};

	var getEntitySummary = function getEntitySummary(data) {
	    var topicID = getTopicID(data);
	    var topic = void 0;
	    var kind = void 0;
	    var id = void 0;

	    if (topicID) {
	        topic = data.topics && data.topics[topicID];
	        kind = topic.entity_kind;
	        id = topic.entity_id;
	    } else {
	        kind = data.routeQuery.kind;
	        id = data.routeQuery.id;
	    }

	    var entity = getEntityByKind(data, kind, id);

	    return {
	        name: entity && entity.name,
	        kind: kind
	    };
	};

	module.exports = function (data) {
	    var topicID = getTopicID(data);
	    var topic = void 0;
	    if (topicID) {
	        topic = data.topics && data.topics[topicID];
	    }

	    if (topicID && !topic) {
	        return spinner();
	    }

	    var formData = extend({}, data.formData, {
	        'topic.id': topic && topic.id,
	        'topic.name': topic && topic.name,
	        'topic.entity_kind': topic && topic.entity_kind || data.routeQuery.kind,
	        'topic.entity_id': topic && topic.entity_id || data.routeQuery.id
	    });

	    var fields = getFields(formData);

	    var schema = prefixObjectKeys('topic.', topicSchema);

	    if (!formData['topic.id']) {
	        fields = fields.concat(getPostFields(formData));
	        extend(schema, getPostSchema(formData));
	    }
	    fields.push({
	        type: 'submit',
	        name: 'submit',
	        label: topicID ? 'Update Topic' : 'Create Topic',
	        icon: 'create'
	    });

	    var instanceFields = createFieldsData({
	        schema: schema,
	        fields: fields,
	        errors: data.errors,
	        formData: formData,
	        sending: data.sending
	    });

	    var globalErrors = findGlobalErrors({
	        fields: fields,
	        errors: data.errors
	    });

	    var entity = getEntitySummary(data);

	    return div({
	        id: 'topic-form',
	        className: classes(formData)
	    }, h1(topicID ? 'Update Topic' : 'Create Topic'), p(strong(ucfirst(entity && entity.kind || '')), ': ' + (entity && entity.name)), form({
	        fields: instanceFields,
	        errors: globalErrors
	    }));
	};

/***/ },
/* 144 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	// TODO-2 add `available` field
	// TODO-2 on update: how to decline a proposal?
	// TODO-3 Tags (all)

	var _require = __webpack_require__(9),
	    extend = _require.extend;

	var _require2 = __webpack_require__(7),
	    prefixObjectKeys = _require2.prefixObjectKeys;

	var postSchema = __webpack_require__(145);
	var voteSchema = __webpack_require__(146);
	var proposalSchema = __webpack_require__(147);

	var schemas = {
	    post: postSchema,
	    vote: voteSchema,
	    proposal: proposalSchema
	};

	var getFields = function getFields(formData) {
	    var fields = [];['post.id', 'post.topic_id', 'post.replies_to_id'].forEach(function (name) {
	        if (formData[name]) {
	            fields.push({ name: name });
	        }
	    }

	    /* PP@ fields.push({
	        name: 'post.kind',
	        options: [{
	            label: 'Post',
	            disabled: !!formData['post.id'],
	        }, {
	            label: 'Proposal',
	            disabled: !!formData['post.id'],
	        }, {
	            label: 'Vote',
	            disabled: !!formData['post.id'] ||
	                      !formData['post.replies_to_id']
	        }],
	        inline: true,
	        label: 'Post Kind'
	    }) */

	    );fields.push({
	        name: 'post.kind',
	        type: 'hidden'
	    });

	    if (formData['post.kind'] === 'vote') {
	        fields.push({
	            name: 'post.response',
	            options: [{ label: 'Yes, I agree' }, { label: 'No, I dissent' }],
	            inline: true,
	            label: 'Response',
	            disabled: !!formData['post.id']
	        });
	    }

	    fields.push({
	        name: 'post.body',
	        label: formData['post.kind'] === 'proposal' ? 'Proposal Summary' : 'Post Body',
	        description: formData['post.kind'] === 'proposal' ? 'Describe the value of this proposal.' : null
	    }

	    // TODO PP@ update proposal handling

	    );return fields;
	};

	var getSchema = function getSchema(formData) {
	    var schema = {};

	    if (formData['post.kind'] === 'proposal') {
	        extend(schema, prefixObjectKeys('post.', schemas.proposal));
	    } else if (formData['post.kind'] === 'vote') {
	        extend(schema, prefixObjectKeys('post.', schemas.vote));
	    } else {
	        extend(schema, prefixObjectKeys('post.', schemas.post));
	    }

	    return schema;
	};

	module.exports = { getFields: getFields, getSchema: getSchema };

/***/ },
/* 145 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(96),
	    required = _require.required;

	module.exports = {
	    id: {
	        type: 'hidden',
	        validations: []
	    },
	    user_id: {
	        type: 'hidden',
	        validations: []
	    },
	    topic_id: {
	        type: 'hidden',
	        validations: []
	    },
	    body: {
	        type: 'textarea',
	        validations: [required]
	    },
	    kind: {
	        type: 'select',
	        options: [{ value: 'post' }, { value: 'proposal' }, { value: 'vote' }],
	        default: 'post',
	        validations: [required]
	    },
	    replies_to_id: {
	        type: 'hidden',
	        validations: []
	    }
	};

/***/ },
/* 146 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var post = __webpack_require__(145);

	var _require = __webpack_require__(9),
	    extend = _require.extend;

	var _require2 = __webpack_require__(96),
	    required = _require2.required;

	var noop = function noop() {};

	module.exports = extend({}, post, {
	    body: {
	        type: 'textarea',
	        validations: [noop]
	    },
	    replies_to_id: {
	        type: 'hidden',
	        validations: [required]
	    },
	    response: {
	        type: 'select',
	        validations: [required],
	        options: [{ value: 'true' }, { value: 'false' }]
	    }
	});

/***/ },
/* 147 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var post = __webpack_require__(145);

	var _require = __webpack_require__(9),
	    extend = _require.extend;

	var _require2 = __webpack_require__(96),
	    required = _require2.required;

	module.exports = extend({}, post, {
	    'entity_version.id': {
	        type: 'hidden',
	        validations: []
	    },
	    'entity_version.kind': {
	        type: 'select',
	        options: [{ value: 'card' }, { value: 'unit' }, { value: 'subject' }],
	        validations: [required]
	    }
	});

/***/ },
/* 148 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(96),
	    required = _require.required;

	module.exports = {
	    id: {
	        type: 'hidden',
	        validations: []
	    },
	    name: {
	        type: 'text',
	        validations: [required]
	    },
	    entity_id: {
	        type: 'hidden',
	        validations: [required]
	    },
	    entity_kind: {
	        type: 'hidden',
	        validations: [required]
	    }
	};

/***/ },
/* 149 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

	var _require = __webpack_require__(78
	// const c = require('../../modules/content').get
	),
	    div = _require.div,
	    h1 = _require.h1;

	var form = __webpack_require__(89);
	var spinner = __webpack_require__(120);

	var _require2 = __webpack_require__(9),
	    extend = _require2.extend;

	var _require3 = __webpack_require__(7),
	    createFieldsData = _require3.createFieldsData,
	    findGlobalErrors = _require3.findGlobalErrors;

	var _require4 = __webpack_require__(144

	// TODO-1 Currently there is no way to update an existing entity from the UI,
	//        you can only propose a new entity.

	),
	    getFields = _require4.getFields,
	    getSchema = _require4.getSchema;

	var classes = function classes(formData) {
	    var postID = formData['post.id'];
	    var postKind = formData['post.kind'];
	    var entityKind = formData['post.entity_version.kind'];
	    var cardKind = formData['entity.kind'];
	    return ['page', postID ? 'update' : 'create', postKind ? 'post-' + postKind : '', entityKind ? 'entity-' + entityKind : '', cardKind ? 'card-' + cardKind : ''].join(' ');
	};

	module.exports = function (data) {
	    var _data$routeArgs = _slicedToArray(data.routeArgs, 2),
	        topicID = _data$routeArgs[0],
	        postID = _data$routeArgs[1];

	    var post = void 0;
	    if (postID) {
	        post = data.topicPosts && data.topicPosts[topicID].find(function (post) {
	            return post.id === postID;
	        });
	    }

	    if (postID && !post) {
	        return spinner();
	    }

	    var formData = extend({}, data.formData, {
	        'post.id': postID,
	        'post.topic_id': topicID,
	        'post.replies_to_id': post && post.replies_to_id || data.routeQuery.replies_to_id,
	        'post.kind': post && post.kind,
	        'post.body': post && post.body,
	        'post.response': post ? '' + post.response : null,
	        'post.name': post && post.name
	    });

	    var fields = getFields(formData);
	    fields.push({
	        type: 'submit',
	        name: 'submit',
	        label: postID ? 'Update Post' : 'Create Post',
	        icon: 'create'
	    });

	    var instanceFields = createFieldsData({
	        schema: getSchema(formData),
	        fields: fields,
	        errors: data.errors,
	        formData: formData,
	        sending: data.sending
	    });

	    var globalErrors = findGlobalErrors({
	        fields: fields,
	        errors: data.errors
	    });

	    return div({
	        id: 'post-form',
	        className: classes(formData)
	    }, h1(postID ? 'Update Post' : 'Create Post'), form({
	        fields: instanceFields,
	        errors: globalErrors
	    }));
	};

/***/ },
/* 150 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78
	// const c = require('../../modules/content').get
	),
	    header = _require.header,
	    h3 = _require.h3,
	    hgroup = _require.hgroup,
	    div = _require.div,
	    h1 = _require.h1,
	    ul = _require.ul,
	    a = _require.a;

	var post = __webpack_require__(151);
	var followButton = __webpack_require__(158);

	var _require2 = __webpack_require__(7),
	    ucfirst = _require2.ucfirst;

	var spinner = __webpack_require__(120);
	var icon = __webpack_require__(91

	// TODO-2 User doesn't show right after creating a new post in the topic view

	);module.exports = function (data) {
	    var id = data.routeArgs[0];
	    var posts = data.topicPosts && data.topicPosts[id];
	    var topic = data.topics && data.topics[id];

	    if (!topic || !posts) {
	        return spinner();
	    }

	    return div({ id: 'topic', className: 'page' }, header(followButton('topic', id, data.follows), hgroup(entity(topic, data), h1(topic.name), data.currentUserID === topic.user_id ? a({ href: '/topics/' + topic.id + '/update' }, icon('update'), ' Update name') : null)), ul({ className: 'posts' }, posts.map(function (postData) {
	        var user = data.users[postData.user_id];
	        return post(Object.assign({}, postData, {
	            user: {
	                name: user && user.name,
	                avatar: data.userAvatars[postData.user_id]
	            },
	            entityVersionsFull: postData.kind === 'proposal' && postData.entity_versions.map(function (ev) {
	                return Object.assign({}, data.topicPostVersions[ev.kind][ev.id], {
	                    entityKind: ev.kind
	                });
	            })
	        }), data.currentUserID);
	    })),
	    // TODO-2 Pagination

	    div({ className: 'topic__actions' }, a({
	        className: 'topic__create',
	        href: '/topics/' + id + '/posts/create'
	    }, icon('create'), ' Create a new post')));
	};

	var entity = function entity(topic, data) {
	    var entityKind = topic.entity_kind;
	    var entityID = topic.entity_id;
	    var entityObj = entityKind === 'card' ? data.cards[entityID] : entityKind === 'unit' ? data.units[entityID] : entityKind === 'subject' ? data.subjects[entityID] : {};
	    var entityName = entityObj && entityObj.name || '';
	    return h3(ucfirst(entityKind) + ': ' + entityName);
	};

/***/ },
/* 151 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    li = _require.li,
	    div = _require.div,
	    img = _require.img,
	    a = _require.a,
	    span = _require.span,
	    h3 = _require.h3,
	    hr = _require.hr;

	var _require2 = __webpack_require__(7),
	    timeAgo = _require2.timeAgo;

	var icon = __webpack_require__(91);
	var previewCard = __webpack_require__(152);
	var previewUnit = __webpack_require__(154);
	var previewSubject = __webpack_require__(156);

	var renderProposal = function renderProposal(data) {
	    if (!data.kind === 'proposal') {
	        return;
	    }
	    var entityVersions = data.entityVersionsFull || [];
	    return div({ className: 'post__proposal' }, entityVersions.map(function (version) {
	        var entityKind = version.entityKind;

	        if (entityKind === 'card') {
	            return [previewCard(Object.assign({}, version, {
	                unit: { name: version.unit_id },
	                requires: version.require_ids && version.require_ids.map(function (id) {
	                    return { id: id };
	                })
	            })), hr()];
	        }
	        if (entityKind === 'unit') {
	            return [previewUnit(Object.assign({}, version, {
	                requires: version.require_ids && version.require_ids.map(function (id) {
	                    return { id: id };
	                })
	            })), hr()];
	        }
	        if (entityKind === 'subject') {
	            return [previewSubject(version), hr()];
	        }
	        return null;
	    }));
	};

	var voteResponse = function voteResponse(response) {
	    if (!response) {
	        return;
	    }
	    return [span({
	        className: 'post__vote--' + (response ? 'good' : 'bad')
	    }, icon(response ? 'good' : 'bad'), response ? ' Yes' : ' No'), ' '];
	};

	module.exports = function (data, currentUserID) {
	    var topicId = data.topic_id;
	    return li({
	        id: data.id,
	        className: 'post'
	    }, div({ className: 'post__avatar' }, a({ href: '/users/' + data.user_id }, img({
	        src: data.user.avatar || '',
	        width: 48,
	        height: 48
	    }))), div({ className: 'post__content' }, div({ className: 'post__when' }, timeAgo(data.created)), a({
	        className: 'post__name',
	        href: '/users/' + data.user_id
	    }, data.user.name || '???'), div(data.replies_to_id ? a({
	        className: 'post__in-reply',
	        href: '/topics/' + data.topic_id + '#' + data.replies_to_id
	    }, icon('reply'), ' In Reply') : null, data.replies_to_id ? ' ' : null, data.kind === 'proposal' ? h3('Proposal') : null, voteResponse(data.response), data.body), data.kind === 'proposal' ? renderProposal(data) : null, div({ className: 'post__footer' }, currentUserID === data.user_id ? a({
	        href: '/topics/' + topicId + '/posts/' + data.id + '/update'
	    }, icon('update'), ' Edit') : a({
	        href: '/topics/' + topicId + '/posts/create?' + ('replies_to_id=' + data.id)
	    }, icon('reply'), ' Reply'),
	    /* PP@ data.kind === 'proposal' ? a(
	        {href: `/topics/${topicId}/posts/create?` +
	               `replies_to_id=${data.id}&kind=vote`},
	        icon('vote'),
	        ' Vote'
	    ) : null, */
	    data.kind === 'proposal' ? a({ href: '/create' }, icon('create'), ' Create Another Proposal') : null, a({ href: '/topics/' + data.topicID + '#' + data.id }, icon('post'), ' Share'
	    // TODO-3 a(
	    //     {href: '#'}
	    //     icon('remove')
	    //     ' Flag'
	    // ) if currentUserID isnt data.user_id
	    ))));
	};

/***/ },
/* 152 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div;

	var previewCardHead = __webpack_require__(104);
	var previewCardContent = __webpack_require__(153);

	module.exports = function previewCard(data) {
	    return div({ className: 'preview--card' }, previewCardHead(data), previewCardContent(data));
	};

/***/ },
/* 153 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable camelcase */
	var _require = __webpack_require__(78),
	    div = _require.div,
	    a = _require.a,
	    iframe = _require.iframe,
	    p = _require.p,
	    ul = _require.ul,
	    li = _require.li,
	    strong = _require.strong,
	    small = _require.small,
	    span = _require.span,
	    em = _require.em,
	    h4 = _require.h4;

	var _require2 = __webpack_require__(7),
	    ucfirst = _require2.ucfirst;

	var _require3 = __webpack_require__(105),
	    previewCommon = _require3.previewCommon,
	    previewRequires = _require3.previewRequires,
	    previewTags = _require3.previewTags;

	var icon = __webpack_require__(91
	// TODO-2 show diff option

	);module.exports = function previewCardContent(_ref) {
	    var kind = _ref.kind,
	        status = _ref.status,
	        available = _ref.available,
	        created = _ref.created,
	        language = _ref.language,
	        unit = _ref.unit,
	        _ref$data = _ref.data;
	    _ref$data = _ref$data === undefined ? {} : _ref$data;
	    var video_id = _ref$data.video_id,
	        site = _ref$data.site,
	        body = _ref$data.body,
	        options = _ref$data.options,
	        order = _ref$data.order,
	        maxOptionsToShow = _ref$data.maxOptionsToShow,
	        requires = _ref.requires,
	        tags = _ref.tags;

	    return div({ className: 'preview--card__content preview--card__content--' + kind }, previewCommon({ created: created, status: status, available: available, language: language }), unit ? h4(unit.url ? a({ href: unit.url }, 'Unit: ', em(unit.name)) : span('Unit: ', em(unit.name))) : null, video_id && site === 'youtube' ? iframe({
	        src: 'https://www.youtube.com/embed/' + video_id + '?autoplay=0&modestbranding=1&rel=0',
	        width: 300,
	        height: 200,
	        allowfullscreen: true
	    }) : null, body ? p(body) : null, options && options.length ? ul(options.map(function (option) {
	        return li(icon(option.correct ? 'good' : 'bad'), ' ', strong(option.value), ' ', small('(' + option.feedback + ')'));
	    })) : null, order ? span('Order: ', em(ucfirst(order))) : null, maxOptionsToShow ? span('Max Options To Show: ', em(maxOptionsToShow)) : null, previewRequires(requires), previewTags(tags));
	};

/***/ },
/* 154 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div;

	var previewUnitHead = __webpack_require__(107);
	var previewUnitContent = __webpack_require__(155);

	module.exports = function previewUnit(data) {
	    return div({ className: 'preview--unit' }, previewUnitHead(data), previewUnitContent(data));
	};

/***/ },
/* 155 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div;

	var _require2 = __webpack_require__(105

	// TODO-2 show diff option

	),
	    previewCommon = _require2.previewCommon,
	    previewRequires = _require2.previewRequires,
	    previewTags = _require2.previewTags;

	module.exports = function previewUnitContent(_ref) {
	    var status = _ref.status,
	        available = _ref.available,
	        created = _ref.created,
	        language = _ref.language,
	        requires = _ref.requires,
	        tags = _ref.tags;

	    return div({ className: 'preview--unit__content' }, previewCommon({ created: created, status: status, available: available, language: language }), previewRequires(requires), previewTags(tags));
	};

/***/ },
/* 156 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div;

	var previewSubjectHead = __webpack_require__(108);
	var previewSubjectContent = __webpack_require__(157);

	module.exports = function previewSubject(data) {
	    return div({ className: 'preview--subject' }, previewSubjectHead(data), previewSubjectContent(data));
	};

/***/ },
/* 157 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    ul = _require.ul,
	    li = _require.li,
	    a = _require.a,
	    h4 = _require.h4,
	    span = _require.span;

	var _require2 = __webpack_require__(105),
	    previewCommon = _require2.previewCommon,
	    previewTags = _require2.previewTags;

	var icon = __webpack_require__(91);

	var _require3 = __webpack_require__(7

	// TODO-2 show diff option

	),
	    ucfirst = _require3.ucfirst;

	module.exports = function previewSubjectContent(_ref) {
	    var status = _ref.status,
	        available = _ref.available,
	        created = _ref.created,
	        language = _ref.language,
	        members = _ref.members,
	        units = _ref.units,
	        tags = _ref.tags;

	    return div({ className: 'preview--subject__content' }, previewCommon({ created: created, status: status, available: available, language: language }), units && units.length ? [h4('List of Units'), ul(units.map(function (unit) {
	        return li(unit.url ? a({ href: unit.url }, unit.name || unit.id) : unit.name || unit.id);
	    }))] : null, members && members.length ? [h4('List of Members'), ul({ className: 'preview--subject__content__members' }, members.map(function (member) {
	        return li(member.kind ? [span({
	            className: 'preview--subject__content__members__kind'
	        }, icon(member.kind), ' ' + ucfirst(member.kind)), ' '] : null, member.url ? a({ href: member.url }, member.name || member.id) : member.name || member.id);
	    }))] : null, previewTags(tags));
	};

/***/ },
/* 158 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    a = _require.a,
	    p = _require.p;

	var icon = __webpack_require__(91);

	module.exports = function (kind, entityId, follows) {
	    var following = follows && follows.find(function (f) {
	        return f.entity_id === entityId;
	    });
	    return following ? p({ className: 'follow-button__following' }, icon('follow'), ' Following') : a({
	        id: kind + '_' + entityId,
	        href: '#',
	        className: 'follow-button'
	    }, icon('follow'), ' Follow');
	};

/***/ },
/* 159 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    p = _require.p,
	    img = _require.img,
	    h3 = _require.h3,
	    header = _require.header,
	    ul = _require.ul,
	    li = _require.li;

	var _require2 = __webpack_require__(7),
	    timeAgo = _require2.timeAgo;

	var spinner = __webpack_require__(120);
	var previewSubjectHead = __webpack_require__(108);
	var previewUnitHead = __webpack_require__(107);
	var previewCardHead = __webpack_require__(104);

	module.exports = function (data) {
	    var _data$routeArgs = _slicedToArray(data.routeArgs, 1),
	        id = _data$routeArgs[0];

	    var user = data.users && data.users[id];
	    if (!user) {
	        return spinner();
	    }

	    return div({ id: 'profile', className: 'page' }, header({ className: 'profile__header' }, img({ src: user.avatar, className: 'profile__avatar' }), h1(user.name), p('Joined ' + timeAgo(user.created))), user.subjects ? showSubjects(user, user.subjects) : null, user.follows ? showFollows(user, user.follows) : null);
	};

	var showSubjects = function showSubjects(user, subjects) {
	    return [h3(user.name + ' is learning:'), ul({ className: 'profile__options' }, subjects.map(function (subject) {
	        return li(previewSubjectHead({
	            url: '/subjects/' + subject.entity_id,
	            name: subject.name,
	            body: subject.body
	        }));
	    }))];
	};
	// TODO-2 and link to search

	var showFollows = function showFollows(user, follows) {
	    return [h3(user.name + ' follows:'), ul({ className: 'profile__options' }, follows.map(function (follow) {
	        var e = follow.entity;
	        var kind = e.kind;
	        return li(kind === 'subject' ? previewSubjectHead({
	            url: '/subjects/' + e.id,
	            name: e.id // TODO-2 update to real name & body
	        }) : kind === 'unit' ? previewUnitHead({
	            url: '/units/' + e.id,
	            name: e.id
	        }) : kind === 'card' ? previewCardHead({
	            url: '/cards/' + e.id,
	            name: e.id
	        }) : kind === 'topic' ? 'topic' // TODO-2
	        : null);
	    }))];
	};

/***/ },
/* 160 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h2 = _require.h2,
	    ul = _require.ul,
	    li = _require.li;

	var spinner = __webpack_require__(120);
	var followButton = __webpack_require__(158);
	var entityHeader = __webpack_require__(161);
	var entityTopics = __webpack_require__(162);
	var entityVersions = __webpack_require__(163);
	var entityRelationships = __webpack_require__(164);

	var assessments = ['choice', 'number', 'match', 'formula', 'writing', 'upload', 'embed'];
	var threeDigits = function threeDigits(num) {
	    return Math.round(num * 1000) / 1000;
	};

	var previewCardContent = __webpack_require__(153);

	module.exports = function (data) {
	    var id = data.routeArgs[0];
	    var card = data.cards && data.cards[id];
	    if (!card) {
	        return spinner();
	    }
	    var cardVersions = data.cardVersions && data.cardVersions[id];

	    var topics = Object.keys(data.topics).filter(function (topicId) {
	        return data.topics[topicId].entity_id === id;
	    }).map(function (topicId) {
	        return data.topics[topicId];
	    });

	    var params = card.card_parameters || {};
	    var assess = card.kind in assessments;
	    return div({ id: 'card', className: 'page' }, followButton('card', card.entity_id, data.follows), entityHeader('card', card), previewCardContent(card), h2('Stats'), ul(li('Number of Learners: ' + params.num_learners), assess ? li('Guess: ' + threeDigits(params.guess)) : null, assess ? li('Slip: ' + threeDigits(params.slip)) : null, li('Transit: ' + threeDigits(params.transit) + ' (Default)')), entityRelationships('card', card), entityTopics('card', card.entity_id, topics), entityVersions('card', card.entity_id, cardVersions));
	};

/***/ },
/* 161 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    header = _require.header,
	    span = _require.span,
	    h1 = _require.h1;

	var _require2 = __webpack_require__(7),
	    ucfirst = _require2.ucfirst;

	var icon = __webpack_require__(91);

	module.exports = function (kind, entity) {
	    var title = ucfirst(kind);
	    if (kind === 'card') {
	        title = ucfirst(entity.kind) + ' ' + title;
	    }

	    return header({ className: 'entity-header' }, span({ className: 'entity-header__kind' }, icon(kind), ' ' + title), h1(entity.name));
	};

/***/ },
/* 162 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    a = _require.a,
	    h2 = _require.h2,
	    ul = _require.ul,
	    li = _require.li,
	    p = _require.p;

	var timeago = __webpack_require__(106);
	var icon = __webpack_require__(91);

	module.exports = function (kind, entityID, topics) {
	    return div({ className: 'entity-topics' }, h2('Topics'), a({
	        href: '/topics/create?kind=' + kind + '&id=' + entityID
	    }, icon('create'), ' Create a new topic'), topics && topics.length ? ul(topics.map(function (topic) {
	        return li(timeago(topic.created, { right: true }),
	        // TODO-2 update time ago to latest post time
	        a({ href: '/topics/' + topic.id }, topic.name
	        // TODO-3 number of posts
	        ));
	    }), li(a({ href: '/search?kind=topic&q=' + entityID }, '... See more topics ', icon('next')))) : null, topics && topics.length ? null : p('No topics yet.'));
	};

/***/ },
/* 163 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    h2 = _require.h2,
	    ul = _require.ul,
	    li = _require.li,
	    span = _require.span,
	    a = _require.a;

	var _require2 = __webpack_require__(7),
	    ucfirst = _require2.ucfirst;

	var timeago = __webpack_require__(106);
	var icon = __webpack_require__(91);

	module.exports = function (kind, entityID, versions) {
	    return [h2('Versions'), ul({ className: 'entity-versions' }, versions && versions.map(function (version) {
	        return li(timeago(version.created, { right: true }), span({
	            className: 'entity-versions__status--' + version.status
	        }, ucfirst(version.status)), ' ', version.name);
	    }), li(a({ href: '/' + kind + 's/' + entityID + '/versions' }, '... See more version history ', icon('next'))))];
	};

/***/ },
/* 164 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    h2 = _require.h2,
	    ul = _require.ul,
	    li = _require.li,
	    a = _require.a;

	var verbage = {
	    requires: 'Requires',
	    required_by: 'Required by',
	    belongs_to: 'Belongs to'

	    // const order = ['card', 'unit', 'subject']

	};module.exports = function (kind, entity) {
	    return [h2('Relationships'), ul(entity.relationships.map(function (relation) {
	        kind = findKind(kind, relation.kind);
	        return li(verbage[relation.kind], ': ', a({ href: '/' + kind + 's/' + relation.entity.entity_id }, relation.entity.name));
	    }))];
	};

	var findKind = function findKind(curr, rel) {
	    if (rel === 'belongs_to') {
	        if (curr === 'unit') {
	            return 'subject';
	        }

	        if (curr === 'card') {
	            return 'unit';
	        }
	    }

	    return curr;
	};

/***/ },
/* 165 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    p = _require.p;

	var followButton = __webpack_require__(158);
	var entityHeader = __webpack_require__(161);
	var entityTopics = __webpack_require__(162);
	var entityVersions = __webpack_require__(163);
	var entityRelationships = __webpack_require__(164);
	var spinner = __webpack_require__(120);
	var previewUnitContent = __webpack_require__(155

	// TODO-2 This page should show a list of cards that the unit contains

	);module.exports = function (data) {
	    var id = data.routeArgs[0];
	    var unit = data.units && data.units[id];

	    if (!unit) {
	        return spinner();
	    }

	    var unitVersions = data.unitVersions && data.unitVersions[id];
	    var topics = Object.keys(data.topics).filter(function (topicId) {
	        return data.topics[topicId].entity_id === id;
	    }).map(function (topicId) {
	        return data.topics[topicId];
	    });

	    return div({ id: 'unit', className: 'page' }, followButton('unit', unit.entity_id, data.follows), entityHeader('unit', unit), p({ className: 'unit__body' }, unit.body), previewUnitContent(Object.assign({}, unit, {
	        requires: unit.require_ids.map(function (id) {
	            return { id: id };
	        })
	    })),
	    /* TODO-2 h2('Stats'),
	    ul(
	        li('Number of Learners: ???'),
	        li('Quality: ???'),
	        li('Difficulty: ???')
	    ), */
	    entityRelationships('unit', unit), entityTopics('unit', unit.entity_id, topics), entityVersions('unit', unit.entity_id, unitVersions));
	};

/***/ },
/* 166 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    p = _require.p,
	    a = _require.a;

	var followButton = __webpack_require__(158);
	var entityHeader = __webpack_require__(161);
	var entityTopics = __webpack_require__(162);
	var entityVersions = __webpack_require__(163);
	var spinner = __webpack_require__(120);
	var icon = __webpack_require__(91);
	var previewSubjectContent = __webpack_require__(157);

	module.exports = function (data) {
	    var id = data.routeArgs[0];
	    var subject = data.subjects && data.subjects[id];

	    if (!subject) {
	        return spinner();
	    }

	    // const following = data.follows &&
	    //            data.follows.find((f) => f.entity_id === subject.entity_id)

	    var subjectVersions = data.subjectVersions && data.subjectVersions[id];
	    var topics = Object.keys(data.topics).filter(function (topicId) {
	        return data.topics[topicId].entity_id === id;
	    }).map(function (topicId) {
	        return data.topics[topicId];
	    });

	    return div({ id: 'subject', className: 'page' }, followButton('subject', subject.entity_id, data.follows), entityHeader('subject', subject), p({ className: 'subject__body' }, subject.body), previewSubjectContent({
	        status: subject.status,
	        available: subject.available,
	        created: subject.created,
	        language: subject.language,
	        members: subject.members, // units and subjects: kind url name id
	        units: subject.units && subject.units.map(function (unit) {
	            return {
	                name: unit.name,
	                url: '/units/' + unit.entity_id
	            };
	        }), // just a list of units: url name id
	        tags: subject.tags
	    }),
	    /* TODO-2 h2('Stats'),
	    ul(
	        li('Number of Learners: ???'),
	        li('Quality: ???'),
	        li('Difficulty: ???')
	    ), */
	    p(a({ href: '/subjects/' + subject.entity_id + '/tree' }, icon('subject'), ' View Unit Tree')), entityTopics('subject', subject.entity_id, topics), entityVersions('subject', subject.entity_id, subjectVersions));
	};

/***/ },
/* 167 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    ul = _require.ul,
	    li = _require.li,
	    p = _require.p,
	    a = _require.a;

	var spinner = __webpack_require__(120);
	var icon = __webpack_require__(91);

	var previewCard = __webpack_require__(152);
	var previewUnit = __webpack_require__(154);
	var previewSubject = __webpack_require__(156

	// TODO-2 Version history and proposal view should have the same layout,
	//        and be similar to the page

	);module.exports = function (data) {
	    var _data$routeArgs = _slicedToArray(data.routeArgs, 2),
	        kind = _data$routeArgs[0],
	        id = _data$routeArgs[1];

	    var versions = data[kind + 'Versions'] && data[kind + 'Versions'][id];
	    if (!versions) {
	        return spinner();
	    }
	    var latestAccepted = versions.find(function (v) {
	        return v.status === 'accepted';
	    });

	    return div({ id: 'versions', className: 'page' }, h1('Versions: ' + latestAccepted.name), p(a({ href: '/' + kind + 's/' + id }, icon('back'), ' See ' + kind + ' page')), ul(versions.map(function (version) {
	        return li(row(kind, version));
	    }))

	    // TODO-2 paginate
	    );
	};

	var row = function row(kind, version) {
	    if (kind === 'card') {
	        return previewCard(Object.assign({}, version, {
	            unit: { name: version.unit_id },
	            requires: version.require_ids.map(function (id) {
	                return { id: id };
	            })
	        }));
	    }

	    if (kind === 'unit') {
	        return previewUnit(Object.assign({}, version, {
	            requires: version.require_ids.map(function (id) {
	                return { id: id };
	            })
	        }));
	    }

	    if (kind === 'subject') {
	        return previewSubject(version);
	    }

	    /* [
	         // Contents
	        ] : kind === 'unit' ? [
	            `Requires: ${version.require_ids.join(', ') || 'None'}`
	        ] :
	     ] */
	};

/***/ },
/* 168 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78
	// const c = require('../../modules/content').get
	// const spinner = require('../components/spinner.tmpl')
	),
	    div = _require.div,
	    h1 = _require.h1,
	    p = _require.p,
	    a = _require.a,
	    ul = _require.ul,
	    li = _require.li;

	var icon = __webpack_require__(91);

	var _require2 = __webpack_require__(9),
	    copy = _require2.copy;

	var previewSubjectHead = __webpack_require__(108);
	var previewUnitHead = __webpack_require__(107);
	var previewCardHead = __webpack_require__(104);

	module.exports = function (data) {
	    // TODO-2 update this to look for some status field
	    // if(!data.follows) { return spinner() }

	    return div({ id: 'follows', className: 'page' }, h1('Follows'), a({ href: '/notices' }, icon('back'), ' Back to notices.'), follows(data.follows.map(function (follow) {
	        var ofKinds = data[follow.entity_kind + 's'] || {};
	        var entity = ofKinds[follow.entity_id];
	        follow = copy(follow);
	        follow.entityFull = entity || {};
	        return follow;
	    })));
	};

	var follows = function follows(data) {
	    if (data.length) {
	        return ul(data.map(function (f) {
	            return follow(f);
	        }));
	    }
	    return p('No follows. ', a({ href: '/search' }, icon('search'), ' Search'));
	};

	var follow = function follow(data) {
	    var kind = data.entity_kind;
	    var _data$entityFull = data.entityFull,
	        name = _data$entityFull.name,
	        body = _data$entityFull.body;

	    return li({ className: 'follow' }, a({
	        id: data.id,
	        href: '#',
	        className: 'follows__unfollow-button'
	    }, icon('remove'), ' Unfollow'), kind === 'unit' ? previewUnitHead({ name: name, body: body, labelKind: true }) : kind === 'subject' ? previewSubjectHead({ name: name, body: body, labelKind: true }) : kind === 'card' ? previewCardHead({
	        name: name,
	        kind: data.entityFull.kind,
	        labelKind: true
	    }) : kind === 'topic' ? 'A topic' : null);
	};

/***/ },
/* 169 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    p = _require.p,
	    ul = _require.ul,
	    li = _require.li,
	    a = _require.a,
	    hr = _require.hr;

	var icon = __webpack_require__(91);
	var spinner = __webpack_require__(120);
	var previewSubjectHead = __webpack_require__(108);

	var subjectResult = function subjectResult(subject) {
	    return [a(
	    // TODO-2 if already in subjects, don't show this button
	    {
	        id: subject.entity_id,
	        href: '#',
	        className: 'add-to-my-subjects'
	    }, icon('create'), ' Add to My Subjects'), div({ className: 'recommended-subjects__right' }, previewSubjectHead({ name: subject.name, body: subject.body }), a({
	        href: '/subjects/' + subject.entity_id + '/tree',
	        className: 'recommended-subjects__view-units'
	    }, icon('unit'), ' View Units'))];
	};

	module.exports = function (data) {
	    if (!data.recommendedSubjects.length) {
	        return spinner();
	    }
	    return div({ id: 'recommended-subjects', className: 'page' }, h1('Recommended Subjects'), p('Want to add a subject here? Email <support@sagefy.org> and let us know!'), ul(data.recommendedSubjects.map(function (subject) {
	        return li(subjectResult(subject));
	    })), hr(), a({ href: '/search?mode=as_learner' }, icon('search'), ' Search Subjects'));
	};

/***/ },
/* 170 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78
	// const c = require('../../modules/content').get
	),
	    div = _require.div,
	    h1 = _require.h1,
	    ul = _require.ul,
	    li = _require.li,
	    p = _require.p,
	    button = _require.button,
	    a = _require.a,
	    br = _require.br;

	var spinner = __webpack_require__(120);
	var icon = __webpack_require__(91);
	var info = __webpack_require__(142);
	var previewSubjectHead = __webpack_require__(108);

	module.exports = function (data) {
	    if (!data.userSubjects) {
	        return spinner();
	    }

	    return div({ id: 'my-subjects', className: 'page' }, h1('My Subjects'), p({ className: 'alert--accent' }, icon('follow'), ' Sagefy is new. You will likely find bugs. ', br(), 'Please report issues to <support@sagefy.org>. ', 'Thank you!'), // TODO-2 Delete this warning message
	    ul({ className: 'my-subjects__list' }, data.userSubjects.map(function (subject) {
	        return userSubject(subject);
	    })), data.userSubjects.length === 0 ? p(a(
	    // TODO-2 temporary {href: '/search?mode=as_learner'},
	    {
	        href: '/recommended_subjects',
	        className: 'my-subjects__find-first-subject'
	    }, icon('search'), ' See Recommended Subjects'), ' to get started.') : p(a(
	    // TODO-2 temporary {href: '/search?mode=as_learner'},
	    { href: '/recommended_subjects' }, icon('search'), ' Find another subject')), info());
	};

	var userSubject = function userSubject(data) {
	    return li({ className: 'my-subject' }, button({
	        className: 'my-subjects__engage-subject',
	        id: data.entity_id
	    }, 'Engage ', icon('next')), div({ className: 'my-subjects__my-subject-right' }, previewSubjectHead({ name: data.name, body: data.body })));
	};

/***/ },
/* 171 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    a = _require.a,
	    p = _require.p;

	var _require2 = __webpack_require__(172),
	    svg = _require2.svg,
	    circle = _require2.circle,
	    line = _require2.line,
	    text = _require2.text;

	var _require3 = __webpack_require__(176),
	    putUnitsInLayers = _require3.putUnitsInLayers,
	    orderLayers = _require3.orderLayers,
	    calculatePoints = _require3.calculatePoints,
	    findUnit = _require3.findUnit;

	var spinner = __webpack_require__(120);
	var icon = __webpack_require__(91

	// TODO-2 show the learner their overall subject progress as a percent or bar

	);var radius = 9;
	var distance = 36;

	module.exports = function (data) {
	    var width = void 0;
	    var id = data.routeArgs[0];
	    var treeData = data.subjectTrees && data.subjectTrees[id];

	    if (!treeData) {
	        return spinner();
	    }

	    var asLearner = data.route.indexOf('as_learner') > -1;
	    var asContrib = !asLearner;

	    var layers = orderLayers(putUnitsInLayers(treeData.units));
	    var nodeHeight = layers.length;
	    var nodeWidth = Math.max.apply(null, layers.map(function (l) {
	        return l.length;
	    }));
	    var preWidth = width = nodeWidth * radius * 2 + (nodeWidth + 1) * distance;
	    if (data.currentTreeUnit) {
	        width += 12 * (6 * 2 + 5);
	    }
	    var height = nodeHeight * radius * 2 + (nodeHeight + 1) * distance;
	    layers = calculatePoints(layers, nodeWidth);

	    var currentUnit = treeData.units.find(function (u) {
	        return u.entity_id === data.currentTreeUnit;
	    });

	    return div({ id: 'tree', className: 'page' }, h1('Tree: ' + treeData.subjects.name), asContrib ? p(a({ href: '/subjects/' + id }, icon('subject'), ' View subject information')) : null, p('You can click the nodes to see the unit name.'), svg({
	        class: 'tree',
	        xmlns: 'http://www.w3.org/2000/svg',
	        version: '1.1',
	        width: width,
	        height: height
	    }, renderLayers({
	        layers: layers,
	        currentUnit: currentUnit,
	        preWidth: preWidth,
	        buckets: treeData.buckets
	    })));
	};

	var renderLayers = function renderLayers(_ref) {
	    var layers = _ref.layers,
	        currentUnit = _ref.currentUnit,
	        preWidth = _ref.preWidth,
	        buckets = _ref.buckets;

	    var nodes = [];
	    // TODO-3 break into smaller functions, and there's lots of repetition..
	    // This is done twice to ensure a line never covers over a circle
	    nodes = nodes.concat(renderLines(layers));
	    nodes = nodes.concat(renderPoints(layers, buckets, currentUnit));
	    nodes = nodes.concat(renderCurrent(layers, currentUnit, preWidth));
	    return nodes;
	};

	var renderLines = function renderLines(layers) {
	    var nodes = [];
	    layers.forEach(function (layer) {
	        layer.forEach(function (unit) {
	            unit.requires.forEach(function (req) {
	                req = findUnit(layers, req);
	                if (req) {
	                    nodes.push(unitLine({
	                        x1: req.x,
	                        y1: req.y,
	                        x2: unit.x,
	                        y2: unit.y
	                    }));
	                }
	            });
	        });
	    });
	    return nodes;
	};

	var renderPoints = function renderPoints(layers, buckets, currentUnit) {
	    var nodes = [];
	    layers.forEach(function (layer) {
	        layer.forEach(function (unit) {
	            Object.keys(buckets).forEach(function (kind) {
	                var bucket = buckets[kind];
	                bucket.forEach(function (id) {
	                    if (id === unit.id) {
	                        unit.className = kind;
	                    }
	                });
	            });
	            nodes.push(unitPoint(unit, currentUnit && currentUnit.entity_id));
	        });
	    });
	    return nodes;
	};

	var renderCurrent = function renderCurrent(layers, currentUnit, preWidth) {
	    var nodes = [];
	    if (!currentUnit) {
	        return nodes;
	    }
	    layers.forEach(function (layer) {
	        layer.forEach(function (unit) {
	            if (unit.id !== currentUnit.entity_id) {
	                return;
	            }
	            nodes.push(line({
	                class: 'name-line',
	                x1: preWidth,
	                y1: unit.y,
	                x2: unit.x + radius,
	                y2: unit.y,
	                'stroke-width': 2
	            }));
	            nodes.push(text({
	                class: 'tree__current-unit',
	                x: preWidth,
	                y: unit.y + 6
	            }, currentUnit.name));
	        });
	    });
	    return nodes;
	};

	var unitPoint = function unitPoint(_ref2, currentTreeUnit) {
	    var id = _ref2.id,
	        x = _ref2.x,
	        y = _ref2.y,
	        className = _ref2.className;
	    return circle({
	        class: className + (currentTreeUnit === id ? ' selected' : ''),
	        id: id,
	        cx: x,
	        cy: y,
	        r: radius
	    });
	};

	var unitLine = function unitLine(_ref3) {
	    var x1 = _ref3.x1,
	        y1 = _ref3.y1,
	        x2 = _ref3.x2,
	        y2 = _ref3.y2;
	    return line({
	        class: 'unit-require',
	        x1: x1,
	        y1: y1,
	        x2: x2,
	        y2: y2,
	        'stroke-width': 2
	    });
	};

/***/ },
/* 172 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var h = __webpack_require__(173

	// https://developer.mozilla.org/en-US/docs/Web/SVG/Element
	);var names = ['svg', 'circle', 'line', 'text'];

	var tags = {};
	var objConstructor = {}.constructor;
	names.forEach(function (name) {
	    tags[name] = function () {
	        for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
	            args[_key] = arguments[_key];
	        }

	        if (args.length === 0) {
	            return h(name);
	        }
	        if (args[0] && args[0].constructor === objConstructor) {
	            return h(name, args[0], args.slice(1));
	        }
	        return h(name, args);
	    };
	});

	module.exports = tags;

/***/ },
/* 173 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var isArray = __webpack_require__(46);

	var h = __webpack_require__(80);


	var SVGAttributeNamespace = __webpack_require__(174);
	var attributeHook = __webpack_require__(175);

	var SVG_NAMESPACE = 'http://www.w3.org/2000/svg';

	module.exports = svg;

	function svg(tagName, properties, children) {
	    if (!children && isChildren(properties)) {
	        children = properties;
	        properties = {};
	    }

	    properties = properties || {};

	    // set namespace for svg
	    properties.namespace = SVG_NAMESPACE;

	    var attributes = properties.attributes || (properties.attributes = {});

	    for (var key in properties) {
	        if (!properties.hasOwnProperty(key)) {
	            continue;
	        }

	        var namespace = SVGAttributeNamespace(key);

	        if (namespace === undefined) { // not a svg attribute
	            continue;
	        }

	        var value = properties[key];

	        if (typeof value !== 'string' &&
	            typeof value !== 'number' &&
	            typeof value !== 'boolean'
	        ) {
	            continue;
	        }

	        if (namespace !== null) { // namespaced attribute
	            properties[key] = attributeHook(namespace, value);
	            continue;
	        }

	        attributes[key] = value
	        properties[key] = undefined
	    }

	    return h(tagName, properties, children);
	}

	function isChildren(x) {
	    return typeof x === 'string' || isArray(x);
	}


/***/ },
/* 174 */
/***/ function(module, exports) {

	'use strict';

	var DEFAULT_NAMESPACE = null;
	var EV_NAMESPACE = 'http://www.w3.org/2001/xml-events';
	var XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink';
	var XML_NAMESPACE = 'http://www.w3.org/XML/1998/namespace';

	// http://www.w3.org/TR/SVGTiny12/attributeTable.html
	// http://www.w3.org/TR/SVG/attindex.html
	var SVG_PROPERTIES = {
	    'about': DEFAULT_NAMESPACE,
	    'accent-height': DEFAULT_NAMESPACE,
	    'accumulate': DEFAULT_NAMESPACE,
	    'additive': DEFAULT_NAMESPACE,
	    'alignment-baseline': DEFAULT_NAMESPACE,
	    'alphabetic': DEFAULT_NAMESPACE,
	    'amplitude': DEFAULT_NAMESPACE,
	    'arabic-form': DEFAULT_NAMESPACE,
	    'ascent': DEFAULT_NAMESPACE,
	    'attributeName': DEFAULT_NAMESPACE,
	    'attributeType': DEFAULT_NAMESPACE,
	    'azimuth': DEFAULT_NAMESPACE,
	    'bandwidth': DEFAULT_NAMESPACE,
	    'baseFrequency': DEFAULT_NAMESPACE,
	    'baseProfile': DEFAULT_NAMESPACE,
	    'baseline-shift': DEFAULT_NAMESPACE,
	    'bbox': DEFAULT_NAMESPACE,
	    'begin': DEFAULT_NAMESPACE,
	    'bias': DEFAULT_NAMESPACE,
	    'by': DEFAULT_NAMESPACE,
	    'calcMode': DEFAULT_NAMESPACE,
	    'cap-height': DEFAULT_NAMESPACE,
	    'class': DEFAULT_NAMESPACE,
	    'clip': DEFAULT_NAMESPACE,
	    'clip-path': DEFAULT_NAMESPACE,
	    'clip-rule': DEFAULT_NAMESPACE,
	    'clipPathUnits': DEFAULT_NAMESPACE,
	    'color': DEFAULT_NAMESPACE,
	    'color-interpolation': DEFAULT_NAMESPACE,
	    'color-interpolation-filters': DEFAULT_NAMESPACE,
	    'color-profile': DEFAULT_NAMESPACE,
	    'color-rendering': DEFAULT_NAMESPACE,
	    'content': DEFAULT_NAMESPACE,
	    'contentScriptType': DEFAULT_NAMESPACE,
	    'contentStyleType': DEFAULT_NAMESPACE,
	    'cursor': DEFAULT_NAMESPACE,
	    'cx': DEFAULT_NAMESPACE,
	    'cy': DEFAULT_NAMESPACE,
	    'd': DEFAULT_NAMESPACE,
	    'datatype': DEFAULT_NAMESPACE,
	    'defaultAction': DEFAULT_NAMESPACE,
	    'descent': DEFAULT_NAMESPACE,
	    'diffuseConstant': DEFAULT_NAMESPACE,
	    'direction': DEFAULT_NAMESPACE,
	    'display': DEFAULT_NAMESPACE,
	    'divisor': DEFAULT_NAMESPACE,
	    'dominant-baseline': DEFAULT_NAMESPACE,
	    'dur': DEFAULT_NAMESPACE,
	    'dx': DEFAULT_NAMESPACE,
	    'dy': DEFAULT_NAMESPACE,
	    'edgeMode': DEFAULT_NAMESPACE,
	    'editable': DEFAULT_NAMESPACE,
	    'elevation': DEFAULT_NAMESPACE,
	    'enable-background': DEFAULT_NAMESPACE,
	    'end': DEFAULT_NAMESPACE,
	    'ev:event': EV_NAMESPACE,
	    'event': DEFAULT_NAMESPACE,
	    'exponent': DEFAULT_NAMESPACE,
	    'externalResourcesRequired': DEFAULT_NAMESPACE,
	    'fill': DEFAULT_NAMESPACE,
	    'fill-opacity': DEFAULT_NAMESPACE,
	    'fill-rule': DEFAULT_NAMESPACE,
	    'filter': DEFAULT_NAMESPACE,
	    'filterRes': DEFAULT_NAMESPACE,
	    'filterUnits': DEFAULT_NAMESPACE,
	    'flood-color': DEFAULT_NAMESPACE,
	    'flood-opacity': DEFAULT_NAMESPACE,
	    'focusHighlight': DEFAULT_NAMESPACE,
	    'focusable': DEFAULT_NAMESPACE,
	    'font-family': DEFAULT_NAMESPACE,
	    'font-size': DEFAULT_NAMESPACE,
	    'font-size-adjust': DEFAULT_NAMESPACE,
	    'font-stretch': DEFAULT_NAMESPACE,
	    'font-style': DEFAULT_NAMESPACE,
	    'font-variant': DEFAULT_NAMESPACE,
	    'font-weight': DEFAULT_NAMESPACE,
	    'format': DEFAULT_NAMESPACE,
	    'from': DEFAULT_NAMESPACE,
	    'fx': DEFAULT_NAMESPACE,
	    'fy': DEFAULT_NAMESPACE,
	    'g1': DEFAULT_NAMESPACE,
	    'g2': DEFAULT_NAMESPACE,
	    'glyph-name': DEFAULT_NAMESPACE,
	    'glyph-orientation-horizontal': DEFAULT_NAMESPACE,
	    'glyph-orientation-vertical': DEFAULT_NAMESPACE,
	    'glyphRef': DEFAULT_NAMESPACE,
	    'gradientTransform': DEFAULT_NAMESPACE,
	    'gradientUnits': DEFAULT_NAMESPACE,
	    'handler': DEFAULT_NAMESPACE,
	    'hanging': DEFAULT_NAMESPACE,
	    'height': DEFAULT_NAMESPACE,
	    'horiz-adv-x': DEFAULT_NAMESPACE,
	    'horiz-origin-x': DEFAULT_NAMESPACE,
	    'horiz-origin-y': DEFAULT_NAMESPACE,
	    'id': DEFAULT_NAMESPACE,
	    'ideographic': DEFAULT_NAMESPACE,
	    'image-rendering': DEFAULT_NAMESPACE,
	    'in': DEFAULT_NAMESPACE,
	    'in2': DEFAULT_NAMESPACE,
	    'initialVisibility': DEFAULT_NAMESPACE,
	    'intercept': DEFAULT_NAMESPACE,
	    'k': DEFAULT_NAMESPACE,
	    'k1': DEFAULT_NAMESPACE,
	    'k2': DEFAULT_NAMESPACE,
	    'k3': DEFAULT_NAMESPACE,
	    'k4': DEFAULT_NAMESPACE,
	    'kernelMatrix': DEFAULT_NAMESPACE,
	    'kernelUnitLength': DEFAULT_NAMESPACE,
	    'kerning': DEFAULT_NAMESPACE,
	    'keyPoints': DEFAULT_NAMESPACE,
	    'keySplines': DEFAULT_NAMESPACE,
	    'keyTimes': DEFAULT_NAMESPACE,
	    'lang': DEFAULT_NAMESPACE,
	    'lengthAdjust': DEFAULT_NAMESPACE,
	    'letter-spacing': DEFAULT_NAMESPACE,
	    'lighting-color': DEFAULT_NAMESPACE,
	    'limitingConeAngle': DEFAULT_NAMESPACE,
	    'local': DEFAULT_NAMESPACE,
	    'marker-end': DEFAULT_NAMESPACE,
	    'marker-mid': DEFAULT_NAMESPACE,
	    'marker-start': DEFAULT_NAMESPACE,
	    'markerHeight': DEFAULT_NAMESPACE,
	    'markerUnits': DEFAULT_NAMESPACE,
	    'markerWidth': DEFAULT_NAMESPACE,
	    'mask': DEFAULT_NAMESPACE,
	    'maskContentUnits': DEFAULT_NAMESPACE,
	    'maskUnits': DEFAULT_NAMESPACE,
	    'mathematical': DEFAULT_NAMESPACE,
	    'max': DEFAULT_NAMESPACE,
	    'media': DEFAULT_NAMESPACE,
	    'mediaCharacterEncoding': DEFAULT_NAMESPACE,
	    'mediaContentEncodings': DEFAULT_NAMESPACE,
	    'mediaSize': DEFAULT_NAMESPACE,
	    'mediaTime': DEFAULT_NAMESPACE,
	    'method': DEFAULT_NAMESPACE,
	    'min': DEFAULT_NAMESPACE,
	    'mode': DEFAULT_NAMESPACE,
	    'name': DEFAULT_NAMESPACE,
	    'nav-down': DEFAULT_NAMESPACE,
	    'nav-down-left': DEFAULT_NAMESPACE,
	    'nav-down-right': DEFAULT_NAMESPACE,
	    'nav-left': DEFAULT_NAMESPACE,
	    'nav-next': DEFAULT_NAMESPACE,
	    'nav-prev': DEFAULT_NAMESPACE,
	    'nav-right': DEFAULT_NAMESPACE,
	    'nav-up': DEFAULT_NAMESPACE,
	    'nav-up-left': DEFAULT_NAMESPACE,
	    'nav-up-right': DEFAULT_NAMESPACE,
	    'numOctaves': DEFAULT_NAMESPACE,
	    'observer': DEFAULT_NAMESPACE,
	    'offset': DEFAULT_NAMESPACE,
	    'opacity': DEFAULT_NAMESPACE,
	    'operator': DEFAULT_NAMESPACE,
	    'order': DEFAULT_NAMESPACE,
	    'orient': DEFAULT_NAMESPACE,
	    'orientation': DEFAULT_NAMESPACE,
	    'origin': DEFAULT_NAMESPACE,
	    'overflow': DEFAULT_NAMESPACE,
	    'overlay': DEFAULT_NAMESPACE,
	    'overline-position': DEFAULT_NAMESPACE,
	    'overline-thickness': DEFAULT_NAMESPACE,
	    'panose-1': DEFAULT_NAMESPACE,
	    'path': DEFAULT_NAMESPACE,
	    'pathLength': DEFAULT_NAMESPACE,
	    'patternContentUnits': DEFAULT_NAMESPACE,
	    'patternTransform': DEFAULT_NAMESPACE,
	    'patternUnits': DEFAULT_NAMESPACE,
	    'phase': DEFAULT_NAMESPACE,
	    'playbackOrder': DEFAULT_NAMESPACE,
	    'pointer-events': DEFAULT_NAMESPACE,
	    'points': DEFAULT_NAMESPACE,
	    'pointsAtX': DEFAULT_NAMESPACE,
	    'pointsAtY': DEFAULT_NAMESPACE,
	    'pointsAtZ': DEFAULT_NAMESPACE,
	    'preserveAlpha': DEFAULT_NAMESPACE,
	    'preserveAspectRatio': DEFAULT_NAMESPACE,
	    'primitiveUnits': DEFAULT_NAMESPACE,
	    'propagate': DEFAULT_NAMESPACE,
	    'property': DEFAULT_NAMESPACE,
	    'r': DEFAULT_NAMESPACE,
	    'radius': DEFAULT_NAMESPACE,
	    'refX': DEFAULT_NAMESPACE,
	    'refY': DEFAULT_NAMESPACE,
	    'rel': DEFAULT_NAMESPACE,
	    'rendering-intent': DEFAULT_NAMESPACE,
	    'repeatCount': DEFAULT_NAMESPACE,
	    'repeatDur': DEFAULT_NAMESPACE,
	    'requiredExtensions': DEFAULT_NAMESPACE,
	    'requiredFeatures': DEFAULT_NAMESPACE,
	    'requiredFonts': DEFAULT_NAMESPACE,
	    'requiredFormats': DEFAULT_NAMESPACE,
	    'resource': DEFAULT_NAMESPACE,
	    'restart': DEFAULT_NAMESPACE,
	    'result': DEFAULT_NAMESPACE,
	    'rev': DEFAULT_NAMESPACE,
	    'role': DEFAULT_NAMESPACE,
	    'rotate': DEFAULT_NAMESPACE,
	    'rx': DEFAULT_NAMESPACE,
	    'ry': DEFAULT_NAMESPACE,
	    'scale': DEFAULT_NAMESPACE,
	    'seed': DEFAULT_NAMESPACE,
	    'shape-rendering': DEFAULT_NAMESPACE,
	    'slope': DEFAULT_NAMESPACE,
	    'snapshotTime': DEFAULT_NAMESPACE,
	    'spacing': DEFAULT_NAMESPACE,
	    'specularConstant': DEFAULT_NAMESPACE,
	    'specularExponent': DEFAULT_NAMESPACE,
	    'spreadMethod': DEFAULT_NAMESPACE,
	    'startOffset': DEFAULT_NAMESPACE,
	    'stdDeviation': DEFAULT_NAMESPACE,
	    'stemh': DEFAULT_NAMESPACE,
	    'stemv': DEFAULT_NAMESPACE,
	    'stitchTiles': DEFAULT_NAMESPACE,
	    'stop-color': DEFAULT_NAMESPACE,
	    'stop-opacity': DEFAULT_NAMESPACE,
	    'strikethrough-position': DEFAULT_NAMESPACE,
	    'strikethrough-thickness': DEFAULT_NAMESPACE,
	    'string': DEFAULT_NAMESPACE,
	    'stroke': DEFAULT_NAMESPACE,
	    'stroke-dasharray': DEFAULT_NAMESPACE,
	    'stroke-dashoffset': DEFAULT_NAMESPACE,
	    'stroke-linecap': DEFAULT_NAMESPACE,
	    'stroke-linejoin': DEFAULT_NAMESPACE,
	    'stroke-miterlimit': DEFAULT_NAMESPACE,
	    'stroke-opacity': DEFAULT_NAMESPACE,
	    'stroke-width': DEFAULT_NAMESPACE,
	    'surfaceScale': DEFAULT_NAMESPACE,
	    'syncBehavior': DEFAULT_NAMESPACE,
	    'syncBehaviorDefault': DEFAULT_NAMESPACE,
	    'syncMaster': DEFAULT_NAMESPACE,
	    'syncTolerance': DEFAULT_NAMESPACE,
	    'syncToleranceDefault': DEFAULT_NAMESPACE,
	    'systemLanguage': DEFAULT_NAMESPACE,
	    'tableValues': DEFAULT_NAMESPACE,
	    'target': DEFAULT_NAMESPACE,
	    'targetX': DEFAULT_NAMESPACE,
	    'targetY': DEFAULT_NAMESPACE,
	    'text-anchor': DEFAULT_NAMESPACE,
	    'text-decoration': DEFAULT_NAMESPACE,
	    'text-rendering': DEFAULT_NAMESPACE,
	    'textLength': DEFAULT_NAMESPACE,
	    'timelineBegin': DEFAULT_NAMESPACE,
	    'title': DEFAULT_NAMESPACE,
	    'to': DEFAULT_NAMESPACE,
	    'transform': DEFAULT_NAMESPACE,
	    'transformBehavior': DEFAULT_NAMESPACE,
	    'type': DEFAULT_NAMESPACE,
	    'typeof': DEFAULT_NAMESPACE,
	    'u1': DEFAULT_NAMESPACE,
	    'u2': DEFAULT_NAMESPACE,
	    'underline-position': DEFAULT_NAMESPACE,
	    'underline-thickness': DEFAULT_NAMESPACE,
	    'unicode': DEFAULT_NAMESPACE,
	    'unicode-bidi': DEFAULT_NAMESPACE,
	    'unicode-range': DEFAULT_NAMESPACE,
	    'units-per-em': DEFAULT_NAMESPACE,
	    'v-alphabetic': DEFAULT_NAMESPACE,
	    'v-hanging': DEFAULT_NAMESPACE,
	    'v-ideographic': DEFAULT_NAMESPACE,
	    'v-mathematical': DEFAULT_NAMESPACE,
	    'values': DEFAULT_NAMESPACE,
	    'version': DEFAULT_NAMESPACE,
	    'vert-adv-y': DEFAULT_NAMESPACE,
	    'vert-origin-x': DEFAULT_NAMESPACE,
	    'vert-origin-y': DEFAULT_NAMESPACE,
	    'viewBox': DEFAULT_NAMESPACE,
	    'viewTarget': DEFAULT_NAMESPACE,
	    'visibility': DEFAULT_NAMESPACE,
	    'width': DEFAULT_NAMESPACE,
	    'widths': DEFAULT_NAMESPACE,
	    'word-spacing': DEFAULT_NAMESPACE,
	    'writing-mode': DEFAULT_NAMESPACE,
	    'x': DEFAULT_NAMESPACE,
	    'x-height': DEFAULT_NAMESPACE,
	    'x1': DEFAULT_NAMESPACE,
	    'x2': DEFAULT_NAMESPACE,
	    'xChannelSelector': DEFAULT_NAMESPACE,
	    'xlink:actuate': XLINK_NAMESPACE,
	    'xlink:arcrole': XLINK_NAMESPACE,
	    'xlink:href': XLINK_NAMESPACE,
	    'xlink:role': XLINK_NAMESPACE,
	    'xlink:show': XLINK_NAMESPACE,
	    'xlink:title': XLINK_NAMESPACE,
	    'xlink:type': XLINK_NAMESPACE,
	    'xml:base': XML_NAMESPACE,
	    'xml:id': XML_NAMESPACE,
	    'xml:lang': XML_NAMESPACE,
	    'xml:space': XML_NAMESPACE,
	    'y': DEFAULT_NAMESPACE,
	    'y1': DEFAULT_NAMESPACE,
	    'y2': DEFAULT_NAMESPACE,
	    'yChannelSelector': DEFAULT_NAMESPACE,
	    'z': DEFAULT_NAMESPACE,
	    'zoomAndPan': DEFAULT_NAMESPACE
	};

	module.exports = SVGAttributeNamespace;

	function SVGAttributeNamespace(value) {
	  if (SVG_PROPERTIES.hasOwnProperty(value)) {
	    return SVG_PROPERTIES[value];
	  }
	}


/***/ },
/* 175 */
/***/ function(module, exports) {

	'use strict';

	module.exports = AttributeHook;

	function AttributeHook(namespace, value) {
	    if (!(this instanceof AttributeHook)) {
	        return new AttributeHook(namespace, value);
	    }

	    this.namespace = namespace;
	    this.value = value;
	}

	AttributeHook.prototype.hook = function (node, prop, prev) {
	    if (prev && prev.type === 'AttributeHook' &&
	        prev.value === this.value &&
	        prev.namespace === this.namespace) {
	        return;
	    }

	    node.setAttributeNS(this.namespace, prop, this.value);
	};

	AttributeHook.prototype.unhook = function (node, prop, next) {
	    if (next && next.type === 'AttributeHook' &&
	        next.namespace === this.namespace) {
	        return;
	    }

	    var colonPosition = prop.indexOf(':');
	    var localName = colonPosition > -1 ? prop.substr(colonPosition + 1) : prop;
	    node.removeAttributeNS(this.namespace, localName);
	};

	AttributeHook.prototype.type = 'AttributeHook';


/***/ },
/* 176 */
/***/ function(module, exports) {

	"use strict";

	var radius = 9;
	var distance = 36;

	var putUnitsInLayers = function putUnitsInLayers(units) {
	    var ids = units.map(function (unit) {
	        return unit.entity_id;
	    });
	    var us = units.map(function (unit) {
	        // eslint-disable-line
	        return {
	            id: unit.entity_id,
	            requires: unit.require_ids.filter(function (id) {
	                return ids.indexOf(id) > -1;
	            })
	        };
	    });
	    var layers = [];
	    var layer = 0;
	    while (us.length) {
	        Object.keys(us).forEach(function (i) {
	            var u = us[i];
	            if (!u.requires.length) {
	                layers[layer] = layers[layer] || [];
	                var unit = units.find(function (unit) {
	                    return unit.entity_id === u.id;
	                });
	                layers[layer].push({
	                    id: unit.entity_id,
	                    requires: unit.require_ids
	                });
	            }
	        });
	        us = us.filter(function (u) {
	            return u.requires.length;
	        });
	        layers[layer].forEach(function (u) {
	            us.forEach(function (o) {
	                var index = o.requires.indexOf(u.id);
	                if (index > -1) {
	                    o.requires.splice(index, 1);
	                }
	            });
	        });
	        layer++;
	    }
	    return layers;
	};

	var orderLayers = function orderLayers(layers) {
	    return layers;
	};
	// TODO-2 reorder the layers to make the lines more efficient

	var calculatePoints = function calculatePoints(layers, nodeWidth) {
	    layers.forEach(function (layer, i) {
	        layer.forEach(function (unit, j) {
	            unit.x = distance + radius + j * (distance + radius * 2) + (nodeWidth - layer.length) * (radius * 2 + distance) / 2;
	            unit.y = i * (distance + radius * 2) + distance + radius;
	        });
	    });
	    return layers;
	};

	var findUnit = function findUnit(layers, id) {
	    var _iteratorNormalCompletion = true;
	    var _didIteratorError = false;
	    var _iteratorError = undefined;

	    try {
	        for (var _iterator = layers[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
	            var layer = _step.value;
	            var _iteratorNormalCompletion2 = true;
	            var _didIteratorError2 = false;
	            var _iteratorError2 = undefined;

	            try {
	                for (var _iterator2 = layer[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
	                    var unit = _step2.value;

	                    if (unit.id === id) {
	                        return unit;
	                    }
	                }
	            } catch (err) {
	                _didIteratorError2 = true;
	                _iteratorError2 = err;
	            } finally {
	                try {
	                    if (!_iteratorNormalCompletion2 && _iterator2.return) {
	                        _iterator2.return();
	                    }
	                } finally {
	                    if (_didIteratorError2) {
	                        throw _iteratorError2;
	                    }
	                }
	            }
	        }
	    } catch (err) {
	        _didIteratorError = true;
	        _iteratorError = err;
	    } finally {
	        try {
	            if (!_iteratorNormalCompletion && _iterator.return) {
	                _iterator.return();
	            }
	        } finally {
	            if (_didIteratorError) {
	                throw _iteratorError;
	            }
	        }
	    }
	};

	var findLayer = function findLayer(layers, id) {
	    var output = void 0;
	    layers.forEach(function (layer, i) {
	        layer.forEach(function (unit) {
	            if (unit.id === id) {
	                output = i;
	                return;
	            }
	        });
	    });
	    return output;
	};

	module.exports = {
	    putUnitsInLayers: putUnitsInLayers,
	    orderLayers: orderLayers,
	    calculatePoints: calculatePoints,
	    findUnit: findUnit,
	    findLayer: findLayer
	};

/***/ },
/* 177 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78
	// const c = require('../../modules/content').get
	),
	    div = _require.div,
	    h1 = _require.h1,
	    ul = _require.ul,
	    li = _require.li,
	    a = _require.a,
	    h3 = _require.h3,
	    span = _require.span,
	    hgroup = _require.hgroup;

	var spinner = __webpack_require__(120);
	var icon = __webpack_require__(91);
	var previewUnitHead = __webpack_require__(107);

	module.exports = function (data) {
	    if (!Object.keys(data.chooseUnit).length) {
	        return spinner();
	    }
	    return div({ id: 'choose-unit', className: 'page' }, Object.keys(data.unitLearned).length ? hgroup(h1('Choose a Unit'), h3(icon('good'), ' You just finished a unit! Pick the next one to learn:')) : h1('Choose a Unit'), ul({ id: data.chooseUnit.subject.entity_id, className: 'units' }, data.chooseUnit.units.slice(0, 5).map(function (unit, index) {
	        return li({ className: index === 0 ? 'recommended' : null }, a({
	            id: unit.entity_id,
	            className: 'choose-unit__engage' + (index === 0 ? ' choose-unit__engage--first' : '')
	        }, 'Engage ', icon('next')), div(index === 0 ? span({ className: 'choose-unit__recommended' }, icon('learn'), ' Recommended') : null, previewUnitHead({
	            name: unit.name,
	            body: unit.body
	        }
	        // TODO-2 % learned
	        )));
	    })));
	};

/***/ },
/* 178 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    a = _require.a,
	    p = _require.p;

	var _require2 = __webpack_require__(9),
	    isNumber = _require2.isNumber;

	var spinner = __webpack_require__(120
	// const c = require('../../modules/content').get
	);var icon = __webpack_require__(91);

	var kindTmpl = {};
	kindTmpl.video = __webpack_require__(179);
	kindTmpl.choice = __webpack_require__(180);

	module.exports = function (data) {
	    var id = data.routeArgs[0];
	    var card = data.learnCards && data.learnCards[id];

	    if (!card) {
	        return spinner();
	    }

	    var pLearned = data.unitLearned && data.unitLearned[card.unit_id];

	    var mode = void 0;
	    if (card.kind === 'video') {
	        mode = 'next-please';
	    } else if (card.kind === 'choice') {
	        if (isNumber(data.cardResponse.score)) {
	            mode = 'next-please';
	        } else {
	            mode = 'answer';
	        }
	    }

	    var feedbackLabel = void 0;
	    if (isNumber(data.cardResponse.score)) {
	        if (data.cardResponse.score === 1) {
	            feedbackLabel = 'good';
	        } else {
	            feedbackLabel = 'bad';
	        }
	    } else {
	        feedbackLabel = 'accent';
	    }

	    return [div({
	        id: 'card-learn',
	        className: 'page ' + card.kind + ' ' + mode,
	        key: 'WbrGhHy5aUCmBVtHnlmTdJ1x'
	    }, kind(card, mode), data.cardFeedback ? p({ className: 'card-learner__feedback--' + feedbackLabel }, icon(feedbackLabel), ' ', data.cardFeedback) : null, p(a({
	        id: id,
	        className: 'continue card-learner__continue'
	    }, 'Continue ', icon('next')))), pLearned ? div({
	        key: '0Xe4fksADWwm9qWOMuTl7thD',
	        className: 'card-learn__progress',
	        style: {
	            width: pLearned * 100 + '%'
	        }
	    }) : null];
	};

	var kind = function kind(card, mode) {
	    if (card.kind === 'video') {
	        return kindTmpl.video(card, mode);
	    }
	    if (card.kind === 'choice') {
	        return kindTmpl.choice(card, mode);
	    }
	};

/***/ },
/* 179 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    iframe = _require.iframe;

	module.exports = function (data) {
	    return iframe({
	        className: 'video',
	        src: data.data.site === 'youtube' ? 'https://www.youtube.com/embed/' + data.data.video_id + '?autoplay=1&modestbranding=1&rel=0' : data.data.site === 'vimeo' ? 'https://player.vimeo.com/video/' + data.data.video_id : '',
	        width: 672,
	        height: 336,
	        allowfullscreen: true
	    });
	};

/***/ },
/* 180 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    ul = _require.ul,
	    li = _require.li,
	    input = _require.input,
	    label = _require.label;

	module.exports = function (data, mode) {
	    var _data$data = data.data,
	        body = _data$data.body,
	        options = _data$data.options;

	    var disabled = mode === 'next-please';

	    return [div(body), ul({ className: 'options card-learn__options' }, options.map(function (option) {
	        return li({ className: disabled ? 'disabled' : '' }, input({
	            type: 'radio',
	            name: 'choice',
	            value: option.id,
	            id: option.id,
	            disabled: disabled,
	            key: data.id + '-' + option.id
	            // The key ensures the input doesn't stay selected
	            // when changing questions
	        }), label({
	            htmlFor: option.id,
	            disabled: disabled
	        }, option.value));
	    }))];
	};

/***/ },
/* 181 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable max-len */
	var _require = __webpack_require__(78),
	    div = _require.div,
	    header = _require.header,
	    h1 = _require.h1,
	    a = _require.a,
	    p = _require.p,
	    section = _require.section,
	    h2 = _require.h2,
	    h3 = _require.h3,
	    ul = _require.ul,
	    li = _require.li,
	    strong = _require.strong,
	    small = _require.small,
	    span = _require.span;

	var icon = __webpack_require__(91);

	module.exports = function (data) {
	    var id = data.routeArgs[0];

	    if (id !== 'JAFGYFWhILcsiByyH2O9frcU') {
	        return div();
	    }

	    var cta = a({
	        href: '/sign_up?subject_id=' + id,
	        className: 'subjects-landing__cta'
	    }, icon('sign-up'), " Let's Get Learning!");

	    var w = function w(n) {
	        return span({ className: 'subjects-landing__icon-wrap' }, n);
	    };

	    return div({
	        id: 'subjects-landing',
	        className: 'page'
	    }, header(h1('An Introduction to Electronic Music'), p('A small taste of the basics of electronic music. Learn the concepts behind creating and modifying sounds in an electronic music system. Learn the ideas behind the tools and systems we use to create electronic music.'), cta, ' – Forever free.'
	    // TODO-2 social media sharing links
	    ), section(h2('Goals'), h3('Who'), p('This subject is for anyone who wants to learn the basic ideas of electronic music systems. We will focus on computer-based systems.'), h3('Outcome'), p("You will be able to explain the basic properties of sound and hearing in a digital system. You'll be able to describe the basic tools of creating and modifying sounds. You'll have an understanding of some of the systems we use to create and edit electronic music."), p('This subject does not teach how to use a particular piece of software. The ideas here will apply to any software of your choice. This subject does not detail: the artistic study of electronic music, the history of electronic music, or how western music theory applies to electronic music. These are important topics, but outside of the scope of this focused subject.'), h3('Requirements'), p('This subject does not require extra software. This subject focuses on the what and why, not how. The ideas apply to any electronic music software, such as Pure Data, Audacity, and Ardour. A background in western music theory is not required.'), p('A basic understanding of mathematical concepts, such as linear vs logarithmic scale, is helpful. Some physics knowledge is also helpful, but not necessary.'), h3('Difficulty'), p('Easy. Approximately 5-10 hours in length.'), h3('Cost'), p('Always free.'), cta), section(h2('About Sagefy'), ul({ className: 'subjects-landing__about-sagefy' }, li(w(icon('next')), ' Short, informational videos. Easy to understand.'), li(w(icon('learn')), ' Lots of practice questions to help you master the content.'), li(w(icon('settings')), ' Sagefy adapts practice questions based on your responses.'), li(w(icon('grow')), ' Completely self-paced.'), li(w(icon('subject')), ' Choose your own path.'), li(w(icon('fast')), ' Skip content you already know.'), li(w(icon('post')), ' Get support with our built-in discussions.')), cta), section(h2('What You Will Learn'), ul(li(h3('Foundation'), ul(li(strong('Electronic Music'), ': Define electronic music and the subjects electronic music covers'), li(strong('Sound Parameters'), ': Describe the basic parameters of sound: amplitude, frequency, duration, phase, and timbre.'), li(strong('Human Hearing'), ': Describe common properties of human hearing, as hearing pertains to electronic music. (Frequency, Amplitude, Spatialization, Hidden Fundamental...)'), li(strong('Hearing Curves'), ': Describe how hearing varies with frequency and amplitude.'), li(strong('Digital Representation'), ': Describe how we represent sound digitally, including bit depth and sample rate.'), li(strong('Analog to Digital'), ': Describe how we convert analog sound into digital sound. (Recording, Nyquist)'), li(strong('Complex Waves'), ': Describe the composition of complex sounds.'))), li(h3('Creating Sound'), ul(li(strong('Oscillators'), ': Describe the oscillators and basic wave forms: sine, triangle, square, and sawtooth.'), li(strong('Noise'), ': Describe the types of noise: white, brown, and pink.'), li(strong('Additive Synthesis'), ': Describe how multiple waves produce a single sound.'), li(strong('Subtractive Synthesis'), ': Describe how we can subtract information to produce sound.'), li(strong('Samplers'), ': Describe samplers.'))), li(h3('Changing Sound'), ul(li(strong('Filters'), ': Describe the basic types of filters: low-pass, high-pass, band-reject, and band-pass.'), li(strong('Modulation'), ': Describe modulation of sound signals.'), li(strong('Low Frequency Oscillators'), ': Describe low-frequency oscillators.'), li(strong('Modulation Effects'), ': Describe modulation effects: tremolo, chorus, flange, phase, vibrato.'), li(strong('Amplitude Modifiers'), ': Describe the basic characteristics of amplitude modifiers: gain, compressors, de-essers, expanders, multi-pressors.'), li(strong('Envelopes'), ': Describe how amplitude changes over time (generators: envelopes).'), li(strong('Equalization'), ': Describe equalizers.'), li(strong('Distortion'), ': Describe distortion and applying the effect to a signal.'), li(strong('Delay'), ': Describe delay effects.'), li(strong('Reverberation'), ': Describe reverberation effects.'))), li(h3('Complex Techniques'), ul(li(strong('Fast Fourier Transform'), ': Describe the inputs, outputs, and applications of the Fast Fourier Transform.'), li(strong('Spatialization'), ': Describe acoustic panning and spatialization.'), li(strong('Frequency Modulation Synthesis'), small(' Coming soon!'), ': Describe frequency modulation (FM) synthesis.'), li(strong('Granular Synthesis'), small(' Coming soon!'), ': Describe granular synthesis.'), li(strong('Formant Synthesis'), small(' Coming soon!'), ': Describe formant synthesis.'), li(strong('Physical Modeling'), small(' Coming soon!'), ': Describe physical modeling.'), li(strong('Convolution'), small(' Coming soon!'), ': Describe convolution.'), li(strong('Vocoding'), small(' Coming soon!'), ': Describe vocoding.'))), li(h3('Systems'), ul(li(strong('Basic Synthesizer'), ': Describe a basic synthesizer configuration.'), li(strong('Mixers'), ': Describe a mixer.'), li(strong('Monophony and Polyphony'), ': Describe polyphonic synthesis.'), li(strong('Musical Instrument Digital Interface'), ': Describe the basics of the MIDI protocol.'), li(strong('Open Sound Control'), ': Describe the basics of the OSC protocol.')))), cta), section(h2('About the Instructor'), p("I am Kevin Heis, the founder of Sagefy. I'm interested in real-time, algorithmic electronic music for performance and installation. I hold a Master's in Intermedia Music Technology from the University of Oregon. But more important, I love learning. I love to support others' learning goals too!"), cta
	    // TODO-3 testimonals/reviews (rating)
	    ));
	};

/***/ },
/* 182 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable max-len */
	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    a = _require.a,
	    p = _require.p;

	module.exports = function () {
	    return div({
	        id: 'suggest',
	        className: 'page'
	    }, h1('The Suggest Page is Down Temporarily'), p('A new Suggest page with more capabilities is in progress. ', 'If you have ideas for free online learning courses, ', 'you can share your idea on our ', a({ href: 'https://sagefy.uservoice.com/forums/233394-general' }, 'UserVoice forum'), '.'));
	};

/***/ },
/* 183 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable */

	// TODO-3 move copy to content directory
	var _require = __webpack_require__(78),
	    div = _require.div,
	    header = _require.header,
	    img = _require.img,
	    hgroup = _require.hgroup,
	    h1 = _require.h1,
	    h2 = _require.h2,
	    h3 = _require.h3,
	    h4 = _require.h4,
	    h5 = _require.h5,
	    h6 = _require.h6,
	    p = _require.p,
	    a = _require.a,
	    hr = _require.hr,
	    strong = _require.strong,
	    ul = _require.ul,
	    ol = _require.ol,
	    li = _require.li,
	    iframe = _require.iframe,
	    br = _require.br,
	    footer = _require.footer,
	    span = _require.span,
	    em = _require.em,
	    section = _require.section;

	var icon = __webpack_require__(91);
	var previewSubjectHead = __webpack_require__(108

	// TODO-1 Include unique CTAs throughout

	);module.exports = function (data) {
	    var cta = a({ href: '/sign_up', className: 'home__cta-button' }, icon('sign-up'), ' Sign Up');

	    var w = function w(n) {
	        return span({ className: 'home__icon-wrap' }, n);
	    };

	    return div({ id: 'home', className: 'page' }, header(img({ src: '/astrolabe.svg', className: 'home__logo' }), hgroup(h1('Sagefy'), h3('Learn anything, customized for you.'), h6('...and always free.')), data.currentUserID ? p('Logged in. ', a({ href: '/my_subjects' }, 'My Subjects ', icon('next'))) : null, data.currentUserID ? null : p(a({ href: '/log_in' }, icon('log-in'), ' Log In'), ' or ', a({ href: '/sign_up' }, icon('sign-up'), ' Sign Up'))), data.currentUserID ? null : div(section(hgroup(h2('What is Sagefy?'), h5('Sagefy is an open-content adaptive learning platform.')), p(strong('Adaptive Learning.'), ' Get the most out of your time and effort spent. Sagefy optimizes based on what you already know and what your goal is.'), p(strong('Open-Content.'), ' Anyone can view, share, create, and edit content. Open-content means that Sagefy reaches a range of learning subjects.'), cta), section(h2('Why learn with Sagefy?'), ul({ className: 'home__ul--why' }, li(w(icon('learn')), em(' Learn any subject.')), li(w(icon('create')), em(' Create and edit any content.')), li(w(icon('fast')), em(' Skip what you already know.')), li(w(icon('grow')), em(' Build up to where you need to be.')), li(w(icon('search')), em(' Choose your own path.')), li(w(icon('topic')), em(' Discussion built in.'))), cta), section(h2('How do I learn with Sagefy?'), ol({ className: 'home__ul--how' }, li(img({ src: 'https://i.imgur.com/6Ay09ws.png' }), 'Create an account.'), li(img({ src: 'https://i.imgur.com/T03jwF6.png' }), 'Find and add a subject.'), li(img({ src: 'https://i.imgur.com/FNuekHE.png' }), 'Choose your unit.'), li(img({ src: 'https://i.imgur.com/bT1FOpe.png' }), 'Learn.')), iframe({
	        width: '560',
	        height: '315',
	        src: 'https://www.youtube.com/embed/gFn4Q9tx7Qs',
	        frameborder: '0',
	        allowfullscreen: true
	    }), p('Also check out the in-detail ', a({
	        href: 'https://stories.sagefy.org/why-im-building-sagefy-731eb0ceceea'
	    }, 'article on Medium'), '.'), cta), section(h2('Popular Subjects'), ul({ className: 'home__ul--popular-subjects' }, li(previewSubjectHead({
	        url: '/subjects/JAFGYFWhILcsiByyH2O9frcU/landing',
	        name: 'An Introduction to Electronic Music',
	        body: 'A small taste of the basics of electronic music. Learn the concepts behind creating and modifying sounds in an electronic music system. Learn the ideas behind the tools and systems we use to create electronic music.'
	    }))), cta),
	    // TODO-1 third party validation
	    section(h2('Features'), ul({ className: 'home__ul--features' }, li(w(icon('unit')), strong('Simple'), ' organization. The only kinds of things are: ', ul(li('Subjects -- or courses,'), li('Units -- or learning goals, and'), li('Cards -- small learning experiences.'))), li(w(icon('search')), strong('Choose'), ' your path along the way. Sagefy recommends, but never requires.'), li(w(icon('reply')), 'Keep up to speed with ', strong('review'), ' reminders.'), li(w(icon('follow')), strong('Variety'), ' of types of cards, so you can stay motivated.'), li(w(icon('good')), 'Focus on what you want to learn with ', strong('no distractions.')), li(w(icon('fast')), strong('Skip'), ' content you already know.'), li(w(icon('learn')), 'Learn ', strong('deeply'), ', instead of skimming the top.')), cta), section(h2('Comparison'), ul(li(strong('Classroom'), ': When we adapt the content to what you already know, we keep the motivation going and reduce effort and time. Classrooms are a difficult place to get personal. Sagefy optimizes for what you already know, every time.'), li(strong('Learning Management Systems'), ': Great cost and time savings come from using technology. LMSs are designed to support the classroom model. With Sagefy, you get both the benefits of online learning and a highly personalized experience.'), li(strong('Closed Adaptive Systems'), ': You should be able to pursue your own goals. Closed systems means only select topics are available. An open-content system like Sagefy reaches a range of topics.'), li(strong('Massive Online Courses'), ': MOOCs reach a large range, but offer little adaption and only support expert-created content. Sagefy has no deadlines -- learn when you see fit.'), li(strong('Flash Cards'), ': Flash cards are great for memorizing content. But what about integration and application of knowledge? Sagefy goes deeper than flash cards.')), cta)), footer(ul(li('© Copyright 2017 Sagefy.'), li(a({ href: 'https://docs.sagefy.org/' }, 'Docs')), li(a({ href: 'https://stories.sagefy.org/' }, 'Stories (Blog)')), li(a({
	        href: 'https://sagefy.uservoice.com/forums/233394-general/'
	    }, icon('contact'), ' Support')), li(a({ href: '/terms' }, icon('terms'), ' Privacy & Terms')))));
	};

/***/ },
/* 184 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    div = _require.div,
	    h1 = _require.h1,
	    p = _require.p;

	var c = __webpack_require__(93).get;

	module.exports = function () {
	    return div({ id: 'error', className: 'page' }, [h1('404'), p(c('not_found'))]);
	};

/***/ },
/* 185 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	// TODO-3 move copy to content directory
	var _require = __webpack_require__(78),
	    nav = _require.nav,
	    div = _require.div,
	    a = _require.a,
	    ul = _require.ul;

	var menuItem = __webpack_require__(186);

	var _require2 = __webpack_require__(9),
	    extend = _require2.extend;

	var _require3 = __webpack_require__(7),
	    ucfirst = _require3.ucfirst,
	    underscored = _require3.underscored;

	var icon = __webpack_require__(91

	// TODO-2 add unread count to notices icon

	// A list of all menu items and their configurations
	);var items = {
	    home: { url: '/' },
	    my_subjects: { title: 'My Subjects', icon: 'subject' },
	    log_in: { title: 'Log In', icon: 'log-in' },
	    terms: {},
	    contact: {},
	    notices: {}, // TODO-2 poll and show unread count
	    settings: {},
	    log_out: { url: '#log_out', title: 'Log Out', icon: 'log-out' },
	    search: {},
	    discuss_card: {
	        url: '/search?kind=topic&q={id}',
	        title: 'Discuss Card',
	        icon: 'post'
	    },
	    discuss_unit: {
	        url: '/search?kind=topic&q={id}',
	        title: 'Discuss Unit',
	        icon: 'post'
	    },
	    discuss_subject: {
	        url: '/search?kind=topic&q={id}',
	        title: 'Discuss Subjects',
	        icon: 'post'
	    },
	    create: {}

	    // For items that don't have them
	    // Use the name to populate title and url automatically
	    // And set the default icon to be painfully obviously wrong
	};Object.keys(items).forEach(function (name) {
	    items[name] = extend({
	        name: name,
	        title: ucfirst(name),
	        url: '/' + underscored(name),
	        icon: name
	    }, items[name] || {});
	}

	// For each state, a list of the menu items to appear
	);var menus = {
	    loggedOut: ['home', 'log_in', 'search', 'contact', 'terms'],
	    loggedIn: ['my_subjects', 'search', 'notices', 'create', 'settings', 'contact', 'terms', 'log_out']
	};

	var addContextItems = function addContextItems(menuItems, _ref) {
	    var card = _ref.card,
	        unit = _ref.unit,
	        subject = _ref.subject;

	    menuItems = menuItems.slice();

	    if (card) {
	        var discuss = extend(items.discuss_card);
	        discuss.url = discuss.url.replace('{id}', card);
	        menuItems.push(discuss);
	        return menuItems;
	    }

	    if (unit) {
	        var _discuss = extend(items.discuss_unit);
	        _discuss.url = _discuss.url.replace('{id}', unit);
	        menuItems.push(_discuss);
	        return menuItems;
	    }

	    if (subject) {
	        var _discuss2 = extend(items.discuss_subject);
	        _discuss2.url = _discuss2.url.replace('{id}', subject);
	        menuItems.push(_discuss2);
	        return menuItems;
	    }

	    return menuItems;
	};

	module.exports = function (data) {
	    var menuItems = menus[data.kind].map(function (name) {
	        return items[name];
	    });
	    menuItems = addContextItems(menuItems, data.context);
	    return nav({ className: data.open ? 'menu selected' : 'menu' }, [data.open ? div({ className: 'menu__overlay' }) : null, a({
	        href: '#',
	        className: 'menu__trigger'
	    }, div({ className: 'menu__logo' }), icon('menu'), div({ className: 'menu__label' }, 'Menu')), data.open ? ul({ className: 'menu__items' }, menuItems.map(function (d) {
	        return menuItem(d);
	    })) : null]);
	};

/***/ },
/* 186 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    li = _require.li,
	    a = _require.a,
	    div = _require.div;

	var icon = __webpack_require__(91);

	module.exports = function (data) {
	    return li({ className: 'menu__item' }, a({ href: data.url }, [icon(data.icon), div({ className: 'menu__item__title' }, data.title)]));
	};

/***/ },
/* 187 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(78),
	    a = _require.a;

	var icon = __webpack_require__(91);

	module.exports = function () {
	    return a({
	        href: 'https://sagefy.uservoice.com/forums/233394-general',
	        className: 'feedback'
	    }, icon('contact'), ' Feedback');
	};

/***/ },
/* 188 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	__webpack_require__(189);
	__webpack_require__(194);
	__webpack_require__(195);
	__webpack_require__(196);
	__webpack_require__(197);
	__webpack_require__(198);
	__webpack_require__(199);
	__webpack_require__(200);
	__webpack_require__(201);
	__webpack_require__(202);
	__webpack_require__(203);
	__webpack_require__(204);
	__webpack_require__(205);
	__webpack_require__(206);
	__webpack_require__(207);

/***/ },
/* 189 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch,
	    getState = _require.getState;

	var tasks = __webpack_require__(73);

	var _require2 = __webpack_require__(7),
	    matchesRoute = _require2.matchesRoute;

	var request = __webpack_require__(190);

	module.exports = tasks.add({
	    getCard: function getCard(id) {
	        dispatch({ type: 'GET_CARD', id: id });
	        return request({
	            method: 'GET',
	            url: '/s/cards/' + id,
	            data: {}
	        }).then(function (response) {
	            dispatch({
	                type: 'GET_CARD_SUCCESS',
	                card: response.card,
	                card_parameters: response.card_parameters,
	                unit: response.unit,
	                requires: response.requires,
	                required_by: response.required_by,
	                id: id
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'get card failure',
	                errors: errors
	            });
	        });
	    },
	    getCardForLearn: function getCardForLearn(id) {
	        dispatch({ type: 'RESET_CARD_RESPONSE' });
	        dispatch({ type: 'RESET_CARD_FEEDBACK' });
	        dispatch({ type: 'GET_LEARN_CARD', id: id });
	        return request({
	            method: 'GET',
	            url: '/s/cards/' + id + '/learn',
	            data: {}
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_LEARN_CARD',
	                message: 'learn card success',
	                card: response.card,
	                id: id
	            });
	            tasks.updateMenuContext({ card: id });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'learn card failure',
	                errors: errors
	            });
	        });
	    },
	    listCardVersions: function listCardVersions(id) {
	        dispatch({ type: 'LIST_CARD_VERSIONS', id: id });
	        return request({
	            method: 'GET',
	            url: '/s/cards/' + id + '/versions',
	            data: {}
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_CARD_VERSIONS',
	                versions: response.versions,
	                message: 'list card versions success',
	                entity_id: id
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'list card versions failure',
	                errors: errors
	            });
	        });
	    },
	    respondToCard: function respondToCard(id, data) {
	        var goNext = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;

	        dispatch({ type: 'RESPOND_TO_CARD', id: id });
	        dispatch({
	            type: 'SET_SENDING_ON'
	        });
	        return request({
	            method: 'POST',
	            url: '/s/cards/' + id + '/responses',
	            data: data
	        }).then(function (response) {
	            if (response.next) {
	                dispatch({
	                    type: 'SET_NEXT',
	                    next: response.next
	                });
	            }
	            dispatch({
	                type: 'SET_CARD_RESPONSE',
	                message: 'respond to card success',
	                response: response.response
	            });
	            dispatch({
	                type: 'ADD_UNIT_LEARNED',
	                unit_id: response.response.unit_id,
	                learned: response.response.learned
	            });
	            dispatch({
	                type: 'SET_CARD_FEEDBACK',
	                feedback: response.feedback
	            });
	            tasks.updateMenuContext({ card: false });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	            if (goNext) {
	                tasks.nextState();
	            }
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'respond to card failure',
	                errors: errors
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	            if (goNext) {
	                tasks.nextState();
	            }
	        });
	    },
	    nextState: function nextState() {
	        var path = getState().next.path;
	        var args = void 0;
	        args = matchesRoute(path, '/s/cards/{id}/learn');
	        if (args) {
	            tasks.route('/cards/' + args[0] + '/learn');
	        }
	        args = matchesRoute(path, '/s/subjects/{id}/units');
	        if (args) {
	            tasks.route('/subjects/' + args[0] + '/choose_unit');
	        }
	        args = matchesRoute(path, '/s/subjects/{id}/tree');
	        if (args) {
	            tasks.route('/subjects/' + args[0] + '/tree');
	        }
	    },
	    needAnAnswer: function needAnAnswer() {
	        dispatch({
	            type: 'SET_CARD_FEEDBACK',
	            feedback: 'Please provide an answer.'
	        });
	    },
	    createNewCardVersions: function createNewCardVersions(cards) {
	        var count = 0;
	        var total = cards.length;
	        var allResponses = [];
	        return new Promise(function (resolve, reject) {
	            cards.forEach(function (card) {
	                request({
	                    method: 'POST',
	                    url: '/s/cards/versions',
	                    data: card
	                }).then(function (response) {
	                    allResponses.push(response.version);
	                    count++;
	                    if (count === total) {
	                        resolve({ cards: allResponses });
	                    }
	                }).catch(function (errors) {
	                    dispatch({
	                        type: 'SET_ERRORS',
	                        message: 'create new card version failure',
	                        errors: errors
	                    });
	                    reject();
	                });
	            });
	        });
	    }
	});

/***/ },
/* 190 */
/***/ function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(process) {'use strict';

	/* eslint-disable global-require */
	if (typeof XMLHttpRequest !== 'undefined') {
	    // For browsers use XHR adapter
	    module.exports = __webpack_require__(192);
	} else if (typeof process !== 'undefined') {
	    // For node use HTTP adapter
	    module.exports = __webpack_require__(193);
	}
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(191)))

/***/ },
/* 191 */
/***/ function(module, exports) {

	// shim for using process in browser
	var process = module.exports = {};

	// cached from whatever global is present so that test runners that stub it
	// don't break things.  But we need to wrap it in a try catch in case it is
	// wrapped in strict mode code which doesn't define any globals.  It's inside a
	// function because try/catches deoptimize in certain engines.

	var cachedSetTimeout;
	var cachedClearTimeout;

	function defaultSetTimout() {
	    throw new Error('setTimeout has not been defined');
	}
	function defaultClearTimeout () {
	    throw new Error('clearTimeout has not been defined');
	}
	(function () {
	    try {
	        if (typeof setTimeout === 'function') {
	            cachedSetTimeout = setTimeout;
	        } else {
	            cachedSetTimeout = defaultSetTimout;
	        }
	    } catch (e) {
	        cachedSetTimeout = defaultSetTimout;
	    }
	    try {
	        if (typeof clearTimeout === 'function') {
	            cachedClearTimeout = clearTimeout;
	        } else {
	            cachedClearTimeout = defaultClearTimeout;
	        }
	    } catch (e) {
	        cachedClearTimeout = defaultClearTimeout;
	    }
	} ())
	function runTimeout(fun) {
	    if (cachedSetTimeout === setTimeout) {
	        //normal enviroments in sane situations
	        return setTimeout(fun, 0);
	    }
	    // if setTimeout wasn't available but was latter defined
	    if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
	        cachedSetTimeout = setTimeout;
	        return setTimeout(fun, 0);
	    }
	    try {
	        // when when somebody has screwed with setTimeout but no I.E. maddness
	        return cachedSetTimeout(fun, 0);
	    } catch(e){
	        try {
	            // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
	            return cachedSetTimeout.call(null, fun, 0);
	        } catch(e){
	            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
	            return cachedSetTimeout.call(this, fun, 0);
	        }
	    }


	}
	function runClearTimeout(marker) {
	    if (cachedClearTimeout === clearTimeout) {
	        //normal enviroments in sane situations
	        return clearTimeout(marker);
	    }
	    // if clearTimeout wasn't available but was latter defined
	    if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
	        cachedClearTimeout = clearTimeout;
	        return clearTimeout(marker);
	    }
	    try {
	        // when when somebody has screwed with setTimeout but no I.E. maddness
	        return cachedClearTimeout(marker);
	    } catch (e){
	        try {
	            // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
	            return cachedClearTimeout.call(null, marker);
	        } catch (e){
	            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
	            // Some versions of I.E. have different rules for clearTimeout vs setTimeout
	            return cachedClearTimeout.call(this, marker);
	        }
	    }



	}
	var queue = [];
	var draining = false;
	var currentQueue;
	var queueIndex = -1;

	function cleanUpNextTick() {
	    if (!draining || !currentQueue) {
	        return;
	    }
	    draining = false;
	    if (currentQueue.length) {
	        queue = currentQueue.concat(queue);
	    } else {
	        queueIndex = -1;
	    }
	    if (queue.length) {
	        drainQueue();
	    }
	}

	function drainQueue() {
	    if (draining) {
	        return;
	    }
	    var timeout = runTimeout(cleanUpNextTick);
	    draining = true;

	    var len = queue.length;
	    while(len) {
	        currentQueue = queue;
	        queue = [];
	        while (++queueIndex < len) {
	            if (currentQueue) {
	                currentQueue[queueIndex].run();
	            }
	        }
	        queueIndex = -1;
	        len = queue.length;
	    }
	    currentQueue = null;
	    draining = false;
	    runClearTimeout(timeout);
	}

	process.nextTick = function (fun) {
	    var args = new Array(arguments.length - 1);
	    if (arguments.length > 1) {
	        for (var i = 1; i < arguments.length; i++) {
	            args[i - 1] = arguments[i];
	        }
	    }
	    queue.push(new Item(fun, args));
	    if (queue.length === 1 && !draining) {
	        runTimeout(drainQueue);
	    }
	};

	// v8 likes predictible objects
	function Item(fun, array) {
	    this.fun = fun;
	    this.array = array;
	}
	Item.prototype.run = function () {
	    this.fun.apply(null, this.array);
	};
	process.title = 'browser';
	process.browser = true;
	process.env = {};
	process.argv = [];
	process.version = ''; // empty string to avoid regexp issues
	process.versions = {};

	function noop() {}

	process.on = noop;
	process.addListener = noop;
	process.once = noop;
	process.off = noop;
	process.removeListener = noop;
	process.removeAllListeners = noop;
	process.emit = noop;
	process.prependListener = noop;
	process.prependOnceListener = noop;

	process.listeners = function (name) { return [] }

	process.binding = function (name) {
	    throw new Error('process.binding is not supported');
	};

	process.cwd = function () { return '/' };
	process.chdir = function (dir) {
	    throw new Error('process.chdir is not supported');
	};
	process.umask = function() { return 0; };


/***/ },
/* 192 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(9),
	    parseJSON = _require.parseJSON,
	    isString = _require.isString,
	    convertDataToGet = _require.convertDataToGet;

	module.exports = function ajax(_ref) {
	    var method = _ref.method,
	        url = _ref.url,
	        data = _ref.data;

	    method = method.toUpperCase();
	    if (method === 'GET') {
	        url = convertDataToGet(url, data);
	    }
	    var request = new XMLHttpRequest();
	    request.open(method, url, true);
	    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
	    var promise = new Promise(function (resolve, reject) {
	        request.onload = function onload() {
	            if (this.status < 400 && this.status >= 200) {
	                resolve(parseJSON(this.responseText));
	            } else {
	                reject(parseAjaxErrors(this));
	            }
	        };
	        request.onerror = function onerror() {
	            reject(null);
	        };
	    });
	    if (method === 'GET') {
	        request.send();
	    } else {
	        request.send(JSON.stringify(data || {}));
	    }
	    return promise;
	};

	// Try to parse the errors array or just return the error text.
	function parseAjaxErrors(response) {
	    if (!response.responseText) {
	        return null;
	    }
	    var errors = parseJSON(response.responseText);
	    if (isString(errors)) {
	        return errors;
	    }
	    return errors.errors;
	}

/***/ },
/* 193 */
/***/ function(module, exports) {

	module.exports = undefined;

/***/ },
/* 194 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch;

	var tasks = __webpack_require__(73);
	var request = __webpack_require__(190);

	module.exports = tasks.add({
	    listFollows: function listFollows(userId) {
	        var skip = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;
	        var limit = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 50;

	        dispatch({ type: 'LIST_FOLLOWS' });
	        return request({
	            method: 'GET',
	            url: '/s/follows',
	            data: { user_id: userId, skip: skip, limit: limit, entities: true }
	        }).then(function (response) {
	            dispatch({
	                type: 'LIST_FOLLOWS_SUCCESS',
	                follows: response.follows
	            });
	            return tasks.listEntitiesByFollows(response.follows);
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'list follows failure',
	                errors: errors
	            });
	        });
	    },
	    askFollow: function askFollow(entityID) {
	        dispatch({ type: 'ASK_FOLLOW', entityID: entityID });
	        return request({
	            method: 'GET',
	            url: '/s/follows',
	            data: { entity_id: entityID }
	        }).then(function (response) {
	            dispatch({
	                type: 'ASK_FOLLOW_SUCCESS',
	                follows: response.follows,
	                entityID: entityID
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'ask follow failure',
	                errors: errors
	            });
	        });
	    },
	    follow: function follow(data) {
	        dispatch({ type: 'FOLLOW', id: data.entity_id });
	        return request({
	            method: 'POST',
	            url: '/s/follows',
	            data: data
	        }).then(function (response) {
	            dispatch({
	                type: 'FOLLOW_SUCCESS',
	                follow: response.follow
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'follow failure',
	                errors: errors
	            });
	        });
	    },
	    unfollow: function unfollow(id) {
	        dispatch({ type: 'UNFOLLOW', id: id });
	        return request({
	            method: 'DELETE',
	            url: '/s/follows/' + id
	        }).then(function () {
	            dispatch({
	                type: 'UNFOLLOW_SUCCESS',
	                id: id
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'unfollow failure',
	                errors: errors
	            });
	        });
	    }
	});

/***/ },
/* 195 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch;

	var tasks = __webpack_require__(73);

	var _require2 = __webpack_require__(7),
	    validateFormData = _require2.validateFormData;

	module.exports = tasks.add({
	    updateFormData: function updateFormData(data) {
	        dispatch({
	            data: data,
	            message: 'update form data',
	            type: 'SET_FORM_DATA'
	        });
	    },
	    validateForm: function validateForm(data, schema, fields) {
	        var errors = validateFormData(data, schema, fields);
	        if (errors.length) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'validate form - invalid',
	                errors: errors
	            });
	            return errors;
	        }
	        dispatch({ type: 'FORM_IS_VALID' });
	    },
	    addListFieldRow: function addListFieldRow(values, name, columns) {
	        dispatch({
	            type: 'ADD_LIST_FIELD_ROW',
	            message: 'add list field row',
	            values: values,
	            name: name,
	            columns: columns
	        });
	    },
	    removeListFieldRow: function removeListFieldRow(values, name, index) {
	        dispatch({
	            type: 'REMOVE_LIST_FIELD_ROW',
	            message: 'remove list field row',
	            values: values,
	            name: name,
	            index: index
	        });
	    }
	});

/***/ },
/* 196 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch;

	var tasks = __webpack_require__(73);

	module.exports = tasks.add({
	    toggleMenu: function toggleMenu() {
	        dispatch({
	            type: 'TOGGLE_MENU'
	        });
	    },
	    updateMenuContext: function updateMenuContext(_ref) {
	        var card = _ref.card,
	            unit = _ref.unit,
	            subject = _ref.subject;

	        dispatch({
	            type: 'UPDATE_MENU_CONTEXT',
	            card: card,
	            unit: unit,
	            subject: subject
	        });
	    }
	});

/***/ },
/* 197 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch;

	var tasks = __webpack_require__(73);
	var request = __webpack_require__(190);

	module.exports = tasks.add({
	    listNotices: function listNotices() {
	        var limit = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 50;
	        var skip = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;

	        dispatch({ type: 'LIST_NOTICES', limit: limit, skip: skip });
	        return request({
	            method: 'GET',
	            data: { limit: limit, skip: skip },
	            url: '/s/notices'
	        }).then(function (response) {
	            dispatch({
	                type: 'LIST_NOTICES_SUCCESS',
	                message: 'list notices success',
	                limit: limit,
	                skip: skip,
	                notices: response.notices
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'list notices failure',
	                errors: errors
	            });
	        });
	    },
	    markNotice: function markNotice(id) {
	        var read = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;

	        dispatch({ type: 'MARK_NOTICE', id: id, read: read });
	        return request({
	            method: 'PUT',
	            url: '/s/notices/' + id,
	            data: { read: read }
	        }).then(function (response) {
	            dispatch({
	                type: 'MARK_NOTICE_SUCCESS',
	                message: 'mark notice success',
	                id: id,
	                read: read,
	                notice: response.notice
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'mark notice failure',
	                errors: errors
	            });
	        });
	    }
	});

/***/ },
/* 198 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable camelcase */
	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch;

	var tasks = __webpack_require__(73);
	var request = __webpack_require__(190);

	function flatten(arr) {
	    return arr.reduce(function (acc, val) {
	        return acc.concat(Array.isArray(val) ? flatten(val) : val);
	    }, []);
	}

	module.exports = tasks.add({
	    listPostsForTopic: function listPostsForTopic(id) {
	        return tasks.listPosts(id).then(function (response) {
	            var userIds = response.posts.map(function (post) {
	                return post.user_id;
	            });
	            var entityVersions = flatten(response.posts.filter(function (post) {
	                return post.kind === 'proposal';
	            }).map(function (post) {
	                return post.entity_versions;
	            }));
	            return Promise.all([tasks.getTopic(id).then(function (response) {
	                var kind = response.topic.entity_kind;
	                var entityId = response.topic.entity_id;
	                return tasks.getEntity(kind, entityId);
	            }), tasks.listUsers(userIds, { size: 48 }), tasks.listEntityVersionsByTopic(id, entityVersions)]);
	        });
	    },
	    listPosts: function listPosts(id) {
	        dispatch({ type: 'LIST_POSTS', id: id });
	        return request({
	            method: 'GET',
	            url: '/s/topics/' + id + '/posts',
	            data: {}
	        }).then(function (response) {
	            var posts = response.posts;
	            dispatch({
	                type: 'ADD_TOPIC_POSTS',
	                message: 'list posts success',
	                topic_id: id,
	                posts: posts
	            });
	            return response;
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'list posts failure',
	                errors: errors
	            });
	        });
	    },
	    createPost: function createPost(data) {
	        dispatch({
	            type: 'SET_SENDING_ON'
	        });
	        var topicId = data.post.topicId || data.post.topic_id;
	        dispatch({ type: 'CREATE_POST', topicId: topicId });
	        return request({
	            method: 'POST',
	            url: '/s/topics/' + topicId + '/posts',
	            data: data.post
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_TOPIC_POSTS',
	                message: 'create post success',
	                topic_id: topicId,
	                posts: [response.post]
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	            tasks.route('/topics/' + topicId // TODO-2 only when in form
	            );return response;
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'create post failure',
	                errors: errors
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        });
	    },
	    updatePost: function updatePost(data) {
	        dispatch({
	            type: 'SET_SENDING_ON'
	        });
	        var id = data.post.id;

	        var topicId = data.post.topic_id;
	        dispatch({ type: 'UPDATE_POST' });
	        return request({
	            method: 'PUT',
	            url: '/s/topics/' + topicId + '/posts/' + id,
	            data: data.post
	        }).then(function (response) {
	            dispatch({
	                type: 'UPDATE_POST_SUCCESS',
	                topicId: topicId,
	                postId: id,
	                post: response.post
	            });
	            tasks.route('/topics/' + topicId);
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'update post failure',
	                errors: errors
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        });
	    }
	});

/***/ },
/* 199 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch,
	    getState = _require.getState;

	var tasks = __webpack_require__(73);

	var _require2 = __webpack_require__(7),
	    matchesRoute = _require2.matchesRoute,
	    ucfirst = _require2.ucfirst;

	var routes = [{ path: '/settings', task: 'openSettingsRoute' }, { path: '/notices', task: 'listNotices' }, { path: '/users/{id}', task: 'openProfileRoute' }, { path: '/my_subjects', task: 'listUserSubjects' }, { path: '/follows', task: 'listFollows' }, { path: '/units/{id}', task: 'openUnitRoute' }, { path: '/subjects/{id}', task: 'openSubjectRoute' }, { path: '/cards/{id}', task: 'openCardRoute' }, { path: '/{kind}s/{id}/versions', task: 'openVersionsRoute' }, { path: '/topics/create', task: 'openCreateTopic' }, { path: '/topics/{id}/update', task: 'openUpdateTopic' }, { path: '/topics/{id}', task: 'openTopicRoute' }, { path: '/subjects/{id}/tree', task: 'openTreeRoute' }, { path: '/subjects/{id}/choose_unit', task: 'openChooseUnit' }, { path: '/cards/{id}/learn', task: 'openLearnCard' }, { path: '/topics/{id}/posts/{id}/update', task: 'openUpdatePost' }, { path: '/search', task: 'openSearch' }, { path: '/recommended_subjects', task: 'getRecommendedSubjects' }, { path: '/create/unit/find', task: 'openFindSubjectForUnits' }];

	module.exports = tasks.add({
	    onRoute: function onRoute(path) {
	        dispatch({ type: 'RESET_FORM_DATA' });
	        dispatch({ type: 'RESET_ERRORS' });
	        dispatch({ type: 'RESET_SEARCH' });
	        var _iteratorNormalCompletion = true;
	        var _didIteratorError = false;
	        var _iteratorError = undefined;

	        try {
	            for (var _iterator = routes[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
	                var route = _step.value;

	                var args = matchesRoute(path, route.path);
	                if (args) {
	                    return tasks[route.task].apply(null, args);
	                }
	            }
	        } catch (err) {
	            _didIteratorError = true;
	            _iteratorError = err;
	        } finally {
	            try {
	                if (!_iteratorNormalCompletion && _iterator.return) {
	                    _iterator.return();
	                }
	            } finally {
	                if (_didIteratorError) {
	                    throw _iteratorError;
	                }
	            }
	        }
	    },
	    openSettingsRoute: function openSettingsRoute() {
	        if (!getState().currentUserID || !getState().users || !getState().users[getState().currentUserID]) {
	            return tasks.getCurrentUser();
	        }
	    },
	    openProfileRoute: function openProfileRoute(id) {
	        return tasks.getUserForProfile(id, { avatar: 12 * 10 });
	    },
	    openUnitRoute: function openUnitRoute(id) {
	        return Promise.all([tasks.getUnit(id), tasks.listUnitVersions(id), tasks.listTopics({ entity_id: id }), tasks.askFollow(id)]);
	    },
	    openSubjectRoute: function openSubjectRoute(id) {
	        return Promise.all([tasks.getSubject(id), tasks.listSubjectVersions(id), tasks.listTopics({ entity_id: id }), tasks.askFollow(id)]);
	    },
	    openCardRoute: function openCardRoute(id) {
	        return Promise.all([tasks.getCard(id), tasks.listCardVersions(id), tasks.listTopics({ entity_id: id }), tasks.askFollow(id)]);
	    },
	    openVersionsRoute: function openVersionsRoute(kind, id) {
	        return tasks['list' + ucfirst(kind) + 'Versions'](id);
	    },
	    openCreateTopic: function openCreateTopic() {
	        var _getState$routeQuery = getState().routeQuery,
	            kind = _getState$routeQuery.kind,
	            id = _getState$routeQuery.id;

	        return tasks['get' + ucfirst(kind)](id);
	    },
	    openUpdateTopic: function openUpdateTopic(id) {
	        return tasks.listPostsForTopic(id);
	    },
	    openTopicRoute: function openTopicRoute(id) {
	        return Promise.all([tasks.listPostsForTopic(id), tasks.askFollow(id)]);
	    },
	    openTreeRoute: function openTreeRoute(id) {
	        return tasks.getSubjectTree(id);
	    },
	    openChooseUnit: function openChooseUnit(subjectId) {
	        return tasks.getSubjectUnits(subjectId);
	    },
	    openLearnCard: function openLearnCard(id) {
	        return tasks.getCardForLearn(id);
	    },
	    openUpdatePost: function openUpdatePost(topicID /* , postID */) {
	        return tasks.listPostsForTopic(topicID);
	    },
	    openSearch: function openSearch() {
	        var q = getState().routeQuery.q;
	        if (q) {
	            return tasks.search({ q: q });
	        }
	    },
	    openFindSubjectForUnits: function openFindSubjectForUnits() {
	        return tasks.getMyRecentSubjects();
	    }
	});

/***/ },
/* 200 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var tasks = __webpack_require__(73);
	var request = __webpack_require__(190);

	var _require = __webpack_require__(2),
	    getState = _require.getState,
	    dispatch = _require.dispatch;

	module.exports = tasks.add({
	    search: function search(_ref) {
	        var q = _ref.q,
	            kind = _ref.kind,
	            _ref$skip = _ref.skip,
	            skip = _ref$skip === undefined ? 0 : _ref$skip,
	            _ref$limit = _ref.limit,
	            limit = _ref$limit === undefined ? 10 : _ref$limit,
	            order = _ref.order;

	        if (q !== getState().searchQuery) {
	            dispatch({ type: 'RESET_SEARCH' });
	        }
	        dispatch({
	            type: 'SET_SEARCH_QUERY',
	            q: q
	        });
	        return request({
	            method: 'GET',
	            url: '/s/search',
	            data: { q: q, kind: kind, skip: skip, limit: limit, order: order }
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_SEARCH_RESULTS',
	                message: 'search success',
	                results: response.hits
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'search failure',
	                errors: errors
	            });
	        });
	    }
	});

/***/ },
/* 201 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch;

	var tasks = __webpack_require__(73);

	var _require2 = __webpack_require__(7),
	    matchesRoute = _require2.matchesRoute;

	var request = __webpack_require__(190);

	module.exports = tasks.add({
	    getSubject: function getSubject(id) {
	        dispatch({ type: 'GET_SUBJECT', id: id });
	        return request({
	            method: 'GET',
	            url: '/s/subjects/' + id,
	            data: {}
	        }).then(function (response) {
	            var subject = response.subject;
	            subject.unit = response.unit;
	            dispatch({
	                type: 'ADD_SUBJECT',
	                message: 'get subject success',
	                subject: subject
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'get subject failure',
	                errors: errors
	            });
	        });
	    },
	    getRecommendedSubjects: function getRecommendedSubjects() {
	        dispatch({ type: 'GET_RECOMMENDED_SUBJECTS' });
	        return request({
	            method: 'GET',
	            url: '/s/subjects/recommended',
	            data: {}
	        }).then(function (response) {
	            dispatch({
	                type: 'SET_RECOMMENDED_SUBJECTS',
	                message: 'get recommended subjects success',
	                recommendedSubjects: response.subjects
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'get recommended subjects failure',
	                errors: errors
	            });
	        });
	    },
	    listSubjectVersions: function listSubjectVersions(id) {
	        dispatch({ type: 'LIST_SUBJECT_VERSIONS', id: id });
	        return request({
	            method: 'GET',
	            url: '/s/subjects/' + id + '/versions',
	            data: {}
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_SUBJECT_VERSIONS',
	                versions: response.versions,
	                entity_id: id,
	                message: 'list subject versions success'
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'list subject versions failure',
	                errors: errors
	            });
	        });
	    },
	    getSubjectTree: function getSubjectTree(id) {
	        dispatch({ type: 'GET_SUBJECT_TREE', id: id });
	        return request({
	            method: 'GET',
	            url: '/s/subjects/' + id + '/tree',
	            data: {}
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_SUBJECT_TREE',
	                message: 'get subject tree success',
	                tree: response,
	                id: id
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'get subject tree failure',
	                errors: errors
	            });
	        });
	    },
	    selectTreeUnit: function selectTreeUnit(id) {
	        dispatch({
	            type: 'SET_CURRENT_TREE_UNIT',
	            id: id
	        });
	    },
	    getSubjectUnits: function getSubjectUnits(id) {
	        dispatch({ type: 'GET_SUBJECT_UNITS', id: id });
	        return request({
	            method: 'GET',
	            url: '/s/subjects/' + id + '/units',
	            data: {}
	        }).then(function (response) {
	            dispatch({
	                type: 'SET_CHOOSE_UNIT',
	                chooseUnit: response,
	                message: 'get subject units success'
	            });
	            dispatch({
	                type: 'SET_NEXT',
	                next: response.next
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'get subject units failure',
	                errors: errors
	            });
	        });
	    },
	    chooseUnit: function chooseUnit(subjectId, unitId) {
	        dispatch({ type: 'CHOOSE_UNIT', subjectId: subjectId, unitId: unitId });
	        return request({
	            method: 'POST',
	            url: '/s/subjects/' + subjectId + '/units/' + unitId,
	            data: {}
	        }).then(function (response) {
	            dispatch({ type: 'CHOOSE_UNIT_SUCCESS', subjectId: subjectId, unitId: unitId });
	            var next = response.next;

	            dispatch({
	                type: 'SET_NEXT',
	                next: next
	            });
	            tasks.updateMenuContext({
	                subject: subjectId,
	                unit: unitId,
	                card: false
	            });
	            var args = matchesRoute(next.path, '/s/cards/{id}/learn');
	            if (args) {
	                tasks.route('/cards/' + args[0] + '/learn');
	            }
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'choose unit failure',
	                errors: errors
	            });
	        });
	    },
	    getMyRecentSubjects: function getMyRecentSubjects() {
	        dispatch({ type: 'GET_MY_RECENT_SUBJECTS' });
	        return request({
	            method: 'GET',
	            url: '/s/subjects:get_my_recently_created',
	            data: {}
	        }).then(function (response) {
	            dispatch({
	                type: 'SET_MY_RECENT_SUBJECTS',
	                subjects: response.subjects
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'get my recent subjects failure',
	                errors: errors
	            });
	        });
	    },
	    createNewSubjectVersion: function createNewSubjectVersion(data) {
	        dispatch({ type: 'CREATE_NEW_SUBJECT_VERSION' });
	        return request({
	            method: 'POST',
	            url: '/s/subjects/versions',
	            data: data
	        }).then(function (response) {
	            dispatch({ type: 'CREATE_NEW_SUBJECT_VERSION_SUCCESS' });
	            return response;
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'create new subject version failure',
	                errors: errors
	            });
	        });
	    },
	    createExistingSubjectVersion: function createExistingSubjectVersion(data) {
	        dispatch({ type: 'CREATE_EXISTING_SUBJECT_VERSION' });
	        return request({
	            method: 'POST',
	            url: '/s/subjects/' + data.entity_id + '/versions',
	            data: data
	        }).then(function (response) {
	            dispatch({ type: 'CREATE_EXISTING_SUBJECT_VERSION_SUCCESS' });
	            return response;
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'create existing subject version failure',
	                errors: errors
	            });
	        });
	    }
	});

/***/ },
/* 202 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch;

	var tasks = __webpack_require__(73);
	var request = __webpack_require__(190);

	var _require2 = __webpack_require__(9),
	    shallowCopy = _require2.shallowCopy;

	module.exports = tasks.add({
	    getTopic: function getTopic(id) {
	        dispatch({ type: 'GET_TOPIC', id: id });
	        return request({
	            method: 'GET',
	            url: '/s/topics/' + id
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_TOPIC',
	                message: 'create topic success',
	                topic: response.topic,
	                id: response.topic.id
	            });
	            return response;
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'get topic failure',
	                errors: errors
	            });
	        });
	    },
	    listTopics: function listTopics() {
	        var opts = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};

	        dispatch({ type: 'LIST_TOPICS', opts: opts });
	        return request({
	            method: 'GET',
	            url: '/s/topics',
	            data: opts
	        }).then(function (response) {
	            response.topics.forEach(function (topic) {
	                dispatch({
	                    type: 'ADD_TOPIC',
	                    message: 'create topic success',
	                    topic: topic,
	                    id: topic.id
	                });
	            });
	            return response;
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'list topics failure',
	                errors: errors
	            });
	        });
	    },
	    createTopicWithPost: function createTopicWithPost(data) {
	        return tasks.createTopic(data).then(function (response) {
	            var post = shallowCopy(data.post);
	            post.topic_id = response.topic.id;
	            return tasks.createPost({ post: post });
	        });
	    },
	    createTopic: function createTopic(data) {
	        dispatch({
	            type: 'SET_SENDING_ON'
	        });
	        dispatch({ type: 'CREATE_TOPIC' });
	        return request({
	            method: 'POST',
	            url: '/s/topics',
	            data: data.topic
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_TOPIC',
	                message: 'create topic success',
	                topic: response.topic,
	                id: response.topic.id
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	            return response;
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'create topic failure',
	                errors: errors
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        });
	    },
	    updateTopic: function updateTopic(data) {
	        dispatch({ type: 'SET_SENDING_ON' });
	        dispatch({ type: 'UPDATE_TOPIC' });
	        return request({
	            method: 'PUT',
	            url: '/s/topics/' + data.topic.id,
	            data: data.topic
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_TOPIC',
	                topic: response.topic,
	                id: data.topic.id,
	                message: 'update topic success'
	            });
	            tasks.route('/topics/' + data.topic.id);
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'update topic failure',
	                errors: errors
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        });
	    }
	});

/***/ },
/* 203 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch;

	var tasks = __webpack_require__(73);
	var request = __webpack_require__(190);

	module.exports = tasks.add({
	    getUnit: function getUnit(id) {
	        dispatch({ type: 'GET_UNIT', id: id });
	        return request({
	            method: 'GET',
	            url: '/s/units/' + id,
	            data: {}
	        }).then(function (response) {
	            var unit = response.unit;
	            unit.relationships = [];['belongs_to', 'requires', 'required_by'].forEach(function (r) {
	                return response[r].forEach(function (e) {
	                    return unit.relationships.push({
	                        kind: r,
	                        entity: e
	                    });
	                });
	            });
	            dispatch({
	                type: 'ADD_UNIT',
	                message: 'get unit success',
	                unit: unit
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'get unit failure',
	                errors: errors
	            });
	        });
	    },
	    listUnitVersions: function listUnitVersions(id) {
	        dispatch({ type: 'LIST_UNIT_VERSIONS', id: id });
	        return request({
	            method: 'GET',
	            url: '/s/units/' + id + '/versions',
	            data: {}
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_UNIT_VERSIONS',
	                versions: response.versions,
	                entity_id: id,
	                message: 'list unit versions success'
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'list unit versions failure',
	                errors: errors
	            });
	        });
	    },
	    createNewUnitVersions: function createNewUnitVersions(units) {
	        var count = 0;
	        var total = units.length;
	        var allResponses = [];
	        return new Promise(function (resolve, reject) {
	            units.forEach(function (unit) {
	                request({
	                    method: 'POST',
	                    url: '/s/units/versions',
	                    data: unit
	                }).then(function (response) {
	                    allResponses.push(response.version);
	                    count++;
	                    if (count === total) {
	                        resolve({ units: allResponses });
	                    }
	                }).catch(function (errors) {
	                    dispatch({
	                        type: 'SET_ERRORS',
	                        message: 'create new unit version failure',
	                        errors: errors
	                    });
	                    reject();
	                });
	            });
	        });
	    }
	});

/***/ },
/* 204 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch,
	    getState = _require.getState;

	var tasks = __webpack_require__(73);
	var request = __webpack_require__(190);

	module.exports = tasks.add({
	    createUser: function createUser(data) {
	        dispatch({
	            type: 'SET_SENDING_ON'
	        });
	        dispatch({ type: 'CREATE_USER' });

	        var _getState = getState(),
	            routeQuery = _getState.routeQuery;

	        var subjectId = routeQuery.subject_id;
	        return request({
	            method: 'POST',
	            url: '/s/users',
	            data: data
	        }).then(function (response) {
	            dispatch({
	                type: 'SET_CURRENT_USER_ID',
	                currentUserID: response.user.id,
	                message: 'create user success'
	            });
	            return dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        }).then(function () {
	            if (!subjectId) {
	                return;
	            }
	            // if subject_id is a param, auto add to user's subjects
	            return tasks.addUserSubject(subjectId);
	        }).then(function () {
	            // TODO-2 make this a listener
	            window.location = '/my_subjects';
	            // Hard redirect to get the HTTP_ONLY cookie
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'create user failure',
	                errors: errors
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        });
	    },
	    updateUser: function updateUser(data) {
	        dispatch({
	            type: 'SET_SENDING_ON'
	        });
	        dispatch({ type: 'UPDATE_USER', id: data.id });
	        return request({
	            method: 'PUT',
	            url: '/s/users/' + data.id,
	            data: data
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_USER',
	                user: response.user,
	                message: 'update user success'
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'update user failure',
	                errors: errors
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        });
	    },
	    getCurrentUser: function getCurrentUser() {
	        dispatch({ type: 'GET_CURRENT_USER' });
	        return request({
	            method: 'GET',
	            url: '/s/users/current'
	        }).then(function (response) {
	            dispatch({
	                type: 'SET_CURRENT_USER_ID',
	                currentUserID: response.user.id
	            });
	            dispatch({
	                type: 'ADD_USER',
	                user: response.user,
	                message: 'get current user success'
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'get current user failure',
	                errors: errors
	            });
	        });
	    },
	    getUserForProfile: function getUserForProfile(id) {
	        var opts = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

	        return tasks.getUser(id, opts
	        /* .then((/userResponse) => {
	                // const {user} = userResponse
	                const calls = []
	                /*
	                TODO-1 update so that these stores are by user_id
	                otherwise there's no way to tell the difference...
	                if (user.settings.view_follows === 'public') {
	                    calls.push(tasks.listFollows(user.id))
	                }
	                if (user.settings.view_subjects === 'public') {
	                    calls.push(tasks.listUserSubjects(user.id))
	                } /
	                return Promise.all(calls)
	            }) */
	        );
	    },
	    getUser: function getUser(id) {
	        var opts = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

	        dispatch({ type: 'GET_USER', id: id });
	        return request({
	            method: 'GET',
	            url: '/s/users/' + id,
	            data: opts
	        }).then(function (response) {
	            var user = response.user;
	            if (response.avatar) {
	                user.avatar = response.avatar;
	            }
	            dispatch({
	                type: 'ADD_USER',
	                message: 'get user success',
	                user: user
	            });
	            return response;
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'get user failure',
	                errors: errors
	            });
	        });
	    },
	    listUsers: function listUsers(userIds) {
	        var opts = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

	        var size = opts.size || 48;
	        dispatch({ type: 'LIST_USERS', userIds: userIds, size: size });
	        return request({
	            method: 'GET',
	            url: '/s/users',
	            data: {
	                user_ids: userIds.join(','),
	                size: size
	            }
	        }).then(function (response) {
	            var users = response.users;

	            users.forEach(function (user) {
	                dispatch({
	                    type: 'ADD_USER',
	                    message: 'get user success',
	                    user: user
	                });
	            });
	            var avatars = response.avatars;

	            dispatch({
	                type: 'ADD_USER_AVATARS',
	                avatars: avatars
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'list users failure',
	                errors: errors
	            });
	        });
	    },
	    logInUser: function logInUser(data) {
	        dispatch({
	            type: 'SET_SENDING_ON'
	        });
	        dispatch({ type: 'LOG_IN_USER' });
	        return request({
	            method: 'POST',
	            url: '/s/sessions',
	            data: data
	        }).then(function (response) {
	            dispatch({
	                type: 'SET_CURRENT_USER_ID',
	                currentUserID: response.user.id,
	                message: 'log in user success'
	            }
	            // Hard redirect to get the HTTP_ONLY cookie
	            // TODO-2 move to listener
	            );window.location = '/my_subjects';
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'log in user failure',
	                errors: errors
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        });
	    },
	    logOutUser: function logOutUser() {
	        dispatch({
	            type: 'SET_SENDING_ON'
	        });
	        dispatch({ type: 'LOG_OUT_USER' });
	        return request({
	            method: 'DELETE',
	            url: '/s/sessions'
	        }).then(function () {
	            dispatch({
	                type: 'RESET_CURRENT_USER_ID',
	                messsage: 'log out user success'
	            });
	            window.location = '/';
	            // Hard redirect to delete the HTTP_ONLY cookie
	            // TODO-2 move to listener
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'log out user failure',
	                errors: errors
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        });
	    },
	    getUserPasswordToken: function getUserPasswordToken(data) {
	        dispatch({
	            type: 'SET_SENDING_ON'
	        });
	        dispatch({ type: 'GET_PASSWORD_TOKEN' });
	        return request({
	            method: 'POST',
	            url: '/s/password_tokens',
	            data: data
	        }).then(function () {
	            dispatch({
	                type: 'SET_PASSWORD_PAGE_STATE',
	                state: 'inbox',
	                message: 'get password token success'
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'get password token failure',
	                errors: errors
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        });
	    },
	    createUserPassword: function createUserPassword(data) {
	        dispatch({
	            type: 'SET_SENDING_ON'
	        });
	        dispatch({ type: 'CREATE_PASSWORD' });
	        return request({
	            method: 'POST',
	            url: '/s/users/' + data.id + '/password',
	            data: data
	        }).then(function (response) {
	            dispatch({
	                type: 'SET_CURRENT_USER_ID',
	                message: 'create password success',
	                currentUserID: response.user.id
	            }
	            // Hard redirect to get the HTTP_ONLY cookie
	            // TODO-2 move to listener
	            );window.location = '/my_subjects';
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'create password failure',
	                errors: errors
	            });
	            dispatch({
	                type: 'SET_SENDING_OFF'
	            });
	        });
	    }
	});

/***/ },
/* 205 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var tasks = __webpack_require__(73);
	var request = __webpack_require__(190);

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch,
	    getState = _require.getState;

	module.exports = tasks.add({
	    listUserSubjects: function listUserSubjects(userId) {
	        var limit = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 50;
	        var skip = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 0;

	        var userID = userId || getState().currentUserID;
	        dispatch({ type: 'LIST_USER_SUBJECTS' });
	        return request({
	            method: 'GET',
	            url: '/s/users/' + userID + '/subjects',
	            data: { limit: limit, skip: skip }
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_USER_SUBJECTS',
	                subjects: response.subjects,
	                message: 'list user subjects success'
	            });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'list user subjects failure',
	                errors: errors
	            });
	        });
	    },
	    addUserSubject: function addUserSubject(subjectId) {
	        var userID = getState().currentUserID;
	        dispatch({ type: 'ADD_USER_SUBJECT', subjectId: subjectId });
	        return request({
	            method: 'POST',
	            url: '/s/users/' + userID + '/subjects/' + subjectId,
	            data: {}
	        }).then(function (response) {
	            dispatch({
	                type: 'ADD_USER_SUBJECTS',
	                subjects: [response.subject],
	                message: 'add user subject success'
	            });
	            tasks.route('/my_subjects');
	            return response;
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'add user sesubjectt failure',
	                errors: errors
	            });
	            tasks.route('/my_subjects');
	        });
	    },
	    chooseSubject: function chooseSubject(subjectId) {
	        var userID = getState().currentUserID;
	        dispatch({ type: 'CHOOSE_SUBJECT', subjectId: subjectId });
	        return request({
	            method: 'PUT',
	            url: '/s/users/' + userID + '/subjects/' + subjectId,
	            data: {}
	        }).then(function (response) {
	            dispatch({ type: 'CHOOSE_SUBJECT_SUCCESS', subjectId: subjectId });
	            tasks.updateMenuContext({
	                subject: subjectId,
	                unit: false,
	                card: false
	            });
	            dispatch({
	                type: 'SET_NEXT',
	                next: response.next
	            });
	            tasks.route('/subjects/' + subjectId + '/choose_unit');
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'choose subject failure',
	                errors: errors
	            });
	        });
	    },
	    removeUserSubject: function removeUserSubject(subjectId) {
	        var userID = getState().currentUserID;
	        dispatch({ type: 'REMOVE_USER_SUBJECT', subjectId: subjectId });
	        return request({
	            method: 'DELETE',
	            url: '/s/users/' + userID + '/subjects/' + subjectId,
	            data: {}
	        }).then(function () {
	            // TODO-1 remove from the state
	            dispatch({ type: 'REMOVE_USER_SUBJECT_SUCCESS', subjectId: subjectId });
	        }).catch(function (errors) {
	            dispatch({
	                type: 'SET_ERRORS',
	                message: 'remove user subject failure',
	                errors: errors
	            });
	        });
	    }
	});

/***/ },
/* 206 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable camelcase */
	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch,
	    getState = _require.getState;

	var tasks = __webpack_require__(73);

	var _require2 = __webpack_require__(9),
	    copy = _require2.copy;

	module.exports = tasks.add({
	    resetCreate: function resetCreate() {
	        dispatch({ type: 'RESET_CREATE' });
	    },
	    updateCreateRoute: function updateCreateRoute(_ref) {
	        var kind = _ref.kind,
	            step = _ref.step;

	        dispatch({ type: 'UPDATE_CREATE_ROUTE', kind: kind, step: step });
	    },
	    createSubjectData: function createSubjectData(values) {
	        dispatch({
	            type: 'CREATE_SUBJECT_DATA',
	            values: values
	        });
	    },
	    addMemberToCreateSubject: function addMemberToCreateSubject(_ref2) {
	        var kind = _ref2.kind,
	            id = _ref2.id,
	            name = _ref2.name,
	            body = _ref2.body;

	        dispatch({
	            type: 'ADD_MEMBER_TO_CREATE_SUBJECT',
	            kind: kind,
	            id: id,
	            name: name,
	            body: body
	        });
	    },
	    addMemberToAddUnits: function addMemberToAddUnits(_ref3) {
	        var id = _ref3.id,
	            version = _ref3.version,
	            name = _ref3.name,
	            body = _ref3.body,
	            _ref3$language = _ref3.language,
	            language = _ref3$language === undefined ? 'en' : _ref3$language,
	            _ref3$require_ids = _ref3.require_ids,
	            require_ids = _ref3$require_ids === undefined ? [] : _ref3$require_ids;

	        dispatch({
	            type: 'ADD_MEMBER_TO_ADD_UNITS',
	            id: id,
	            version: version,
	            name: name,
	            body: body,
	            language: language,
	            require_ids: require_ids
	        });
	    },
	    addMemberToAddCards: function addMemberToAddCards(values) {
	        dispatch({
	            type: 'ADD_MEMBER_TO_ADD_CARDS',
	            values: values
	        });
	    },
	    removeMemberFromCreateSubject: function removeMemberFromCreateSubject(_ref4) {
	        var id = _ref4.id;

	        // TODO-2 switch to undo
	        if (window.confirm('Remove member?')) {
	            // eslint-disable-line
	            dispatch({
	                type: 'REMOVE_MEMBER_FROM_CREATE_SUBJECT',
	                id: id
	            });
	        }
	    },
	    removeUnitFromSubject: function removeUnitFromSubject(_ref5) {
	        var index = _ref5.index;

	        // TODO-2 switch to undo
	        if (window.confirm('Remove unit?')) {
	            // eslint-disable-line
	            dispatch({
	                type: 'REMOVE_UNIT_FROM_SUBJECT',
	                index: index
	            });
	        }
	    },
	    removeCardFromUnit: function removeCardFromUnit(_ref6) {
	        var index = _ref6.index;

	        // TODO-2 switch to undo
	        if (window.confirm('Remove card?')) {
	            // eslint-disable-line
	            dispatch({
	                type: 'REMOVE_CARD_FROM_UNIT',
	                index: index
	            });
	        }
	    },
	    createChooseSubjectForUnits: function createChooseSubjectForUnits(_ref7) {
	        var id = _ref7.id,
	            name = _ref7.name;

	        dispatch({
	            type: 'CREATE_CHOOSE_SUBJECT_FOR_UNITS',
	            id: id,
	            name: name
	        });
	    },
	    createChooseUnitForCards: function createChooseUnitForCards(_ref8) {
	        var id = _ref8.id,
	            name = _ref8.name;

	        dispatch({
	            type: 'CREATE_CHOOSE_UNIT_FOR_CARDS',
	            id: id,
	            name: name
	        });
	    },
	    stowProposedUnit: function stowProposedUnit(_ref9) {
	        var name = _ref9.name,
	            language = _ref9.language,
	            body = _ref9.body,
	            require_ids = _ref9.require_ids;

	        dispatch({
	            type: 'STOW_PROPOSED_UNIT',
	            name: name,
	            language: language,
	            body: body,
	            require_ids: require_ids
	        });
	    },
	    stowProposedCard: function stowProposedCard(values) {
	        dispatch({
	            type: 'STOW_PROPOSED_CARD',
	            values: values
	        });
	    },
	    addRequireToProposedUnit: function addRequireToProposedUnit(_ref10) {
	        var id = _ref10.id,
	            name = _ref10.name,
	            body = _ref10.body,
	            kind = _ref10.kind;

	        dispatch({
	            type: 'ADD_REQUIRE_TO_PROPOSED_UNIT',
	            id: id,
	            name: name,
	            body: body,
	            kind: kind
	        });
	    },
	    createSubjectProposal: function createSubjectProposal(data) {
	        var topicId = void 0;
	        var subjectId = void 0;
	        tasks.createTopic({ topic: data.topic }).then(function (topicResponse) {
	            topicId = topicResponse.topic.id;
	            return tasks.createNewSubjectVersion(data.subject);
	        }).then(function (subjectResponse) {
	            var post = copy(data.post);
	            post.topic_id = topicId;
	            post.entity_versions = [{
	                kind: 'subject',
	                id: subjectResponse.version.version_id
	            }];
	            subjectId = subjectResponse.version.entity_id;
	            return tasks.createPost({ post: post });
	        }).then(function () {
	            return tasks.route('/subjects/' + subjectId);
	        });
	    },
	    createUnitsProposal: function createUnitsProposal() {
	        var state = getState();
	        var selectedSubject = state.create.selectedSubject;

	        var topic = {
	            name: 'Add Units to This Subject',
	            entity_id: selectedSubject.id,
	            entity_kind: 'subject'
	        };

	        var topicId = void 0;
	        var unitVersionIds = void 0;
	        return tasks.createTopic({ topic: topic }).then(function (topicResponse) {
	            topicId = topicResponse.topic.id;
	            var newUnits = state.create.units.filter(function (unit) {
	                return !unit.id;
	            });
	            return tasks.createNewUnitVersions(newUnits);
	        }).then(function (unitsResponse) {
	            var existingUnitIds = state.create.units.map(function (unit) {
	                return unit.id;
	            }).filter(function (unitId) {
	                return unitId;
	            });
	            var newUnitIds = unitsResponse.units.map(function (unit) {
	                return unit.entity_id;
	            });
	            var unitIds = [].concat(existingUnitIds, newUnitIds);

	            var existingUnitVersionIds = state.create.units.map(function (unit) {
	                return unit.version;
	            }).filter(function (version) {
	                return version;
	            });
	            var newUnitVersionIds = unitsResponse.units.map(function (unit) {
	                return unit.version_id;
	            });
	            unitVersionIds = [].concat(existingUnitVersionIds, newUnitVersionIds);

	            var subject = {
	                entity_id: selectedSubject.id,
	                members: unitIds.map(function (unitId) {
	                    return {
	                        kind: 'unit',
	                        id: unitId
	                    };
	                })
	            };
	            return tasks.createExistingSubjectVersion(subject);
	        }).then(function (subjectResponse) {
	            var post = {
	                kind: 'proposal',
	                body: 'Add Units to Subject',
	                topic_id: topicId,
	                entity_versions: [{
	                    kind: 'subject',
	                    id: subjectResponse.version.version_id
	                }].concat(unitVersionIds.map(function (unitId) {
	                    return {
	                        id: unitId,
	                        kind: 'unit'
	                    };
	                }))
	            };
	            return tasks.createPost({ post: post });
	        }).then(function () {
	            return tasks.route('/subjects/' + selectedSubject.id);
	        });
	    },
	    createCardsProposal: function createCardsProposal() {
	        var state = getState();
	        var selectedUnit = state.create.selectedUnit;

	        var topic = {
	            name: 'Add Cards to This Unit',
	            entity_id: selectedUnit.id,
	            entity_kind: 'unit'
	        };
	        var topicId = void 0;
	        return tasks.createTopic({ topic: topic }).then(function (topicResponse) {
	            topicId = topicResponse.topic.id;
	            var cards = state.create.cards;

	            cards = cards.map(function (card) {
	                return Object.assign({}, card, {
	                    unit_id: selectedUnit.id
	                });
	            });
	            return tasks.createNewCardVersions(cards);
	        }).then(function (cardsResponse) {
	            var post = {
	                kind: 'proposal',
	                body: 'Add Cards to Unit',
	                topic_id: topicId,
	                entity_versions: cardsResponse.cards.map(function (card) {
	                    return {
	                        id: card.version_id,
	                        kind: 'card'
	                    };
	                })
	            };
	            return tasks.createPost({ post: post });
	        }).then(function () {
	            return tasks.route('/units/' + selectedUnit.id);
	        });
	    }
	});

/***/ },
/* 207 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

	var _require = __webpack_require__(2),
	    dispatch = _require.dispatch;

	var tasks = __webpack_require__(73);
	var request = __webpack_require__(190);

	module.exports = tasks.add({
	    getEntity: function getEntity(kind, entityId) {
	        if (kind === 'card') {
	            return tasks.getCard(entityId);
	        } else if (kind === 'unit') {
	            return tasks.getUnit(entityId);
	        } else if (kind === 'subject') {
	            return tasks.getSubject(entityId);
	        }
	    },
	    listEntityVersionsByTopic: function listEntityVersionsByTopic(id, entityVersions) {
	        var total = entityVersions.length;
	        var count = 0;
	        return new Promise(function (resolve, reject) {
	            if (total === 0) {
	                resolve();
	            }
	            entityVersions.forEach(function (ev) {
	                request({
	                    method: 'GET',
	                    url: '/s/' + ev.kind + 's/versions/' + ev.id
	                }).then(function (response) {
	                    var ahh = ev.kind.toUpperCase();
	                    dispatch({
	                        type: 'ADD_TOPIC_POST_VERSIONS_' + ahh,
	                        version: response.version
	                    });
	                    count++;
	                    if (count === total) {
	                        resolve();
	                    }
	                }).catch(function (errors) {
	                    dispatch({
	                        type: 'SET_ERRORS',
	                        message: 'get versions for topic failure',
	                        errors: errors
	                    });
	                    reject();
	                });
	            });
	        });
	        //
	    },
	    listEntitiesByFollows: function listEntitiesByFollows(follows) {
	        var entities = follows.map(function (follow) {
	            return follow.entity;
	        });
	        var total = entities.length;
	        var count = 0;
	        return new Promise(function (resolve, reject) {
	            entities.forEach(function (entity) {
	                request({
	                    method: 'GET',
	                    url: '/s/' + entity.kind + 's/' + entity.id
	                }).then(function (response) {
	                    dispatch(_defineProperty({
	                        type: 'ADD_' + entity.kind.toUpperCase()
	                    }, entity.kind, response[entity.kind]));
	                    count++;
	                    if (count === total) {
	                        resolve();
	                    }
	                }).catch(function (errors) {
	                    dispatch({
	                        type: 'SET_ERRORS',
	                        message: 'list entities follows failure',
	                        errors: errors
	                    });
	                    reject();
	                });
	            });
	        });
	    }
	});

/***/ },
/* 208 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	module.exports = broker.add({
	    // When we click an internal link, use `route` instead
	    'click a[href^="/"]': function clickAHref(e, el) {
	        e.preventDefault();
	        window.scrollTo(0, 0);
	        tasks.route(el.pathname + el.search);
	    },

	    // Do nothing on empty links
	    'click a[href="#"]': function clickAHref(e) {
	        e.preventDefault();
	    },

	    // Open external URLs in new windows
	    'click a[href*="//"]': function clickAHref(e, el) {
	        el.target = '_blank';
	    }
	});

/***/ },
/* 209 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	module.exports = broker.add({
	    'click .follow-button': function clickFollowButton(e, el) {
	        if (e) {
	            e.preventDefault();
	        }

	        var _el$id$split = el.id.split('_'),
	            _el$id$split2 = _slicedToArray(_el$id$split, 2),
	            kind = _el$id$split2[0],
	            id = _el$id$split2[1];

	        tasks.follow({
	            entity_id: id,
	            entity_kind: kind
	        });
	    }
	});

/***/ },
/* 210 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	var _require = __webpack_require__(9),
	    closest = _require.closest;

	var _require2 = __webpack_require__(7),
	    getFormValues = _require2.getFormValues;

	module.exports = broker.add({
	    'click .form-field--list__remove-row': function clickFormFieldList__removeRow(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        var form = closest(el, 'form');
	        var values = getFormValues(form);
	        var table = closest(el, 'table');
	        var name = table.dataset.name;
	        var index = parseInt(el.dataset.index);
	        tasks.removeListFieldRow(values, name, index);
	    },
	    'click .form-field--list__add-row': function clickFormFieldList__addRow(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        var form = closest(el, 'form');
	        var values = getFormValues(form);
	        var table = closest(el, 'table');
	        var name = table.dataset.name;
	        var columns = Array.prototype.map.call(table.querySelectorAll('th'), function (el) {
	            return el.dataset.col;
	        }).filter(function (c) {
	            return c;
	        });
	        tasks.addListFieldRow(values, name, columns);
	    }
	});

/***/ },
/* 211 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71
	// const tasks = require('../../modules/tasks')
	// const {getFormValues} = require('../../modules/auxiliaries')

	);module.exports = broker.add({});

/***/ },
/* 212 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71
	// const tasks = require('../../modules/tasks')
	// const {debounce} = require('../../modules/auxiliaries')

	);module.exports = broker.add({
	    'click .select .clear': function clickSelectClear(e) {
	        e.preventDefault
	        // TODO-3 clear options
	        ();
	    }
	});

/***/ },
/* 213 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	module.exports = broker.add({
	    'click .menu__overlay, .menu__trigger, .menu__item a': function clickMenu__overlayMenu__triggerMenu__itemA(e) {
	        if (e) {
	            e.preventDefault();
	        }
	        tasks.toggleMenu();
	    },
	    'click [href="#log_out"]': function clickHrefLog_out(e) {
	        if (e) {
	            e.preventDefault();
	        }
	        tasks.logOutUser();
	    }
	});

/***/ },
/* 214 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	module.exports = broker.add({
	    'click .notice': function clickNotice(e, el) {
	        if (el.classList.contains('notice--unread')) {
	            tasks.markNotice(el.id);
	        }
	    }
	});

/***/ },
/* 215 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);

	module.exports = broker.add({
	    // TODO-2 request more notices
	});

/***/ },
/* 216 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);

	module.exports = broker.add({
	    'click .post .expand': function clickPostExpand(e) {
	        if (e) {
	            e.preventDefault();
	        }
	        // TODO-2 el
	    }
	});

/***/ },
/* 217 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	var _require = __webpack_require__(9),
	    closest = _require.closest;

	module.exports = broker.add({
	    'click #card-learn.choice.answer .continue': function clickCardLearnChoiceAnswerContinue(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        var container = closest(el, '#card-learn');
	        var checked = container.querySelector('[name=choice]:checked');
	        var response = checked && checked.value;
	        if (response) {
	            tasks.respondToCard(el.id, { response: response });
	        } else {
	            tasks.needAnAnswer();
	        }
	    },
	    'click #card-learn.choice.next-please .continue': function clickCardLearnChoiceNextPleaseContinue(e) {
	        if (e) {
	            e.preventDefault();
	        }
	        tasks.nextState();
	    },
	    'click #card-learn.video .continue': function clickCardLearnVideoContinue(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        tasks.respondToCard(el.id, {}, true);
	    }
	});

/***/ },
/* 218 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);

	module.exports = broker.add({});

/***/ },
/* 219 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	var _require = __webpack_require__(9),
	    closest = _require.closest;

	module.exports = broker.add({
	    'click .choose-unit__engage': function clickChooseUnit__engage(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        var ul = closest(el, 'ul');
	        tasks.chooseUnit(ul.id, el.id);
	    }
	});

/***/ },
/* 220 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);

	module.exports = broker.add({});

/***/ },
/* 221 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	/* eslint-disable no-alert */
	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	module.exports = broker.add({
	    'click .follows__unfollow-button': function clickFollows__unfollowButton(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        // TODO-2 switch to undo
	        if (window.confirm('Unfollow?')) {
	            tasks.unfollow(el.id);
	        }
	    }
	});

/***/ },
/* 222 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	var _require = __webpack_require__(7),
	    getFormValues = _require.getFormValues,
	    parseFormValues = _require.parseFormValues;

	var userSchema = __webpack_require__(110);

	module.exports = broker.add({
	    'submit #log-in form': function submitLogInForm(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        var values = getFormValues(el);
	        tasks.updateFormData(values);
	        var errors = tasks.validateForm(values, userSchema, ['name', 'password']);
	        if (errors && errors.length) {
	            return;
	        }
	        values = parseFormValues(values);
	        tasks.logInUser(values);
	    }
	});

/***/ },
/* 223 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	module.exports = broker.add({
	    'click .my-subjects__engage-subject': function clickMySubjects__engageSubject(e) {
	        if (e) {
	            e.preventDefault();
	        }
	        var entityID = e.target.id;
	        tasks.chooseSubject(entityID);
	    }
	});

/***/ },
/* 224 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	var _require = __webpack_require__(7),
	    getFormValues = _require.getFormValues,
	    parseFormValues = _require.parseFormValues;

	var qs = __webpack_require__(74);
	var userSchema = __webpack_require__(110);

	module.exports = broker.add({
	    'submit #password.email form': function submitPasswordEmailForm(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        var values = getFormValues(el);
	        tasks.updateFormData(values);
	        var errors = tasks.validateForm(values, userSchema, ['email']);
	        if (errors && errors.length) {
	            return;
	        }
	        values = parseFormValues(values);
	        tasks.getUserPasswordToken(values);
	    },
	    'submit #password.password form': function submitPasswordPasswordForm(e, el) {
	        if (e) {
	            e.preventDefault();
	        }

	        var _qs$get = qs.get(),
	            token = _qs$get.token,
	            id = _qs$get.id;

	        var values = getFormValues(el);
	        values.token = token;
	        values.id = id;
	        tasks.updateFormData(values);
	        var errors = tasks.validateForm(values, userSchema, ['password']);
	        if (errors && errors.length) {
	            return;
	        }
	        values = parseFormValues(values);
	        tasks.createUserPassword(values);
	    }
	});

/***/ },
/* 225 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	var _require = __webpack_require__(7),
	    getFormValues = _require.getFormValues,
	    parseFormValues = _require.parseFormValues;

	module.exports = broker.add({
	    'submit #post-form.create form': function submitPostFormCreateForm(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        var values = getFormValues(el);
	        tasks.updateFormData(values
	        // errors = tasks.validateForm(values, schema, [...])
	        // unless errors?.length, (...tab)
	        );values = parseFormValues(values
	        /* PP@ if (values.post && values.post.kind === 'proposal') {
	            if (values.entity && values.entity.require_ids) {
	                values.entity.require_ids = values.entity.require_ids
	                    .map((require) => require.id).filter((require) => require)
	            }
	            if (values.post &&
	                values.post.entity_version
	                && values.post.entity_version.kind) {
	                values[values.post.entity_version.kind] = values.entity
	                delete values.entity
	            }
	        } */
	        );tasks.createPost(values);
	    },
	    'submit #post-form.update form': function submitPostFormUpdateForm(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        var values = getFormValues(el);
	        tasks.updateFormData(values
	        // errors = tasks.validateForm(values, schema, [...])
	        // unless errors?.length, (...tab)
	        );values = parseFormValues(values);
	        tasks.updatePost(values);
	    }
	});

/***/ },
/* 226 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	var _require = __webpack_require__(9),
	    closest = _require.closest;

	module.exports = broker.add({
	    'click #search [type="submit"]': function clickSearchTypeSubmit(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        var form = closest(el, 'form');
	        var input = form.querySelector('input');
	        tasks.search({ q: input.value });
	    },
	    'click .add-to-my-subjects': function clickAddToMySubjects(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        tasks.addUserSubject(el.id);
	    }
	});

/***/ },
/* 227 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);

	module.exports = broker.add({});

/***/ },
/* 228 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	var _require = __webpack_require__(7),
	    getFormValues = _require.getFormValues,
	    parseFormValues = _require.parseFormValues;

	var userSchema = __webpack_require__(110);

	module.exports = broker.add({
	    'submit #settings form': function submitSettingsForm(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        var values = getFormValues(el);
	        tasks.updateFormData(values);
	        var errors = tasks.validateForm(values, userSchema, ['name', 'email']);
	        if (errors && errors.length) {
	            return;
	        }
	        values = parseFormValues(values);
	        tasks.updateUser(values);
	    }
	});

/***/ },
/* 229 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	var _require = __webpack_require__(7),
	    getFormValues = _require.getFormValues,
	    parseFormValues = _require.parseFormValues;

	var userSchema = __webpack_require__(110);

	module.exports = broker.add({
	    'submit #sign-up form': function submitSignUpForm(e, el) {
	        if (e) e.preventDefault();
	        var values = getFormValues(el);
	        tasks.updateFormData(values);
	        var errors = tasks.validateForm(values, userSchema, ['name', 'email', 'password']);
	        if (errors && errors.length) {
	            return;
	        }
	        values = parseFormValues(values);
	        tasks.createUser(values);
	    }
	});

/***/ },
/* 230 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	var _require = __webpack_require__(9),
	    closest = _require.closest;

	var _require2 = __webpack_require__(7),
	    getFormValues = _require2.getFormValues,
	    parseFormValues = _require2.parseFormValues;

	module.exports = broker.add({
	    'submit #topic-form.create form': function submitTopicFormCreateForm(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        var values = getFormValues(el);
	        tasks.updateFormData(values
	        // errors = tasks.validateForm(values, schema, [...])
	        // unless errors?.length, (...tab)
	        );values = parseFormValues(values
	        /* PP@ if (values.post && values.post.kind === 'proposal') {
	            if (values.entity && values.entity.require_ids) {
	                values.entity.require_ids = values.entity.require_ids
	                    .map((require) => require.id).filter((require) => require)
	            }
	            if (values.post &&
	                values.post.entity_version &&
	                values.post.entity_version.kind) {
	                values[values.post.entity_version.kind] = values.entity
	                delete values.entity
	            }
	        } */
	        );tasks.createTopicWithPost(values);
	    },
	    'submit #topic-form.update form': function submitTopicFormUpdateForm(e, el) {
	        if (e) {
	            e.preventDefault();
	        }
	        var values = getFormValues(el);
	        tasks.updateFormData(values
	        // errors = tasks.validateForm(values, schema, [...])
	        // unless errors?.length, (...tab)
	        );values = parseFormValues(values);
	        tasks.updateTopic(values);
	    },
	    'change #topic-form.create [name="post.kind"]': function changeTopicFormCreateNamePostKind(e, el) {
	        var form = closest(el, 'form');
	        var values = getFormValues(form);
	        tasks.updateFormData(values);
	    },
	    'change #topic-form.create [name="post.entity_version.kind"]': function changeTopicFormCreateNamePostEntity_versionKind(e, el) {
	        var form = closest(el, 'form');
	        var values = getFormValues(form);
	        tasks.updateFormData(values);
	    },
	    'change #topic-form.create [name="entity_kind"]': function changeTopicFormCreateNameEntity_kind(e, el) {
	        var form = closest(el, 'form');
	        var values = getFormValues(form);
	        tasks.updateFormData(values);
	    }
	});

/***/ },
/* 231 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71
	// const tasks = require('../../modules/tasks')

	);module.exports = broker.add({
	    'click #topic .follow': function clickTopicFollow(e) {
	        if (e) e.preventDefault
	        // TODO-2 el
	        ();
	    },
	    'click #topic .unfollow': function clickTopicUnfollow(e) {
	        if (e) e.preventDefault
	        // TODO-2 el
	        ();
	    },
	    'click #topic .load-more': function clickTopicLoadMore(e) {
	        if (e) e.preventDefault
	        // TODO-2 el
	        ();
	    }
	});

/***/ },
/* 232 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	module.exports = broker.add({
	    'click .tree circle': function clickTreeCircle(e, el) {
	        if (e) e.preventDefault();
	        if (el.classList.contains('selected')) {
	            tasks.selectTreeUnit();
	        } else {
	            tasks.selectTreeUnit(el.id);
	        }
	    },
	    'click .tree text': function clickTreeText(e) {
	        if (e) e.preventDefault();
	        tasks.selectTreeUnit();
	    }
	});

/***/ },
/* 233 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var broker = __webpack_require__(71);

	module.exports = broker.add({});

/***/ },
/* 234 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

	var broker = __webpack_require__(71);
	var tasks = __webpack_require__(73);

	var _require = __webpack_require__(7),
	    getFormValues = _require.getFormValues,
	    parseFormValues = _require.parseFormValues;

	var subjectSchema = __webpack_require__(126);
	var unitSchema = __webpack_require__(134);
	var cardSchema = __webpack_require__(138);

	var _require2 = __webpack_require__(9),
	    closest = _require2.closest;

	module.exports = broker.add({
	    'click .create__route': function clickCreate__route(e, el) {
	        if (e) e.preventDefault();

	        var _el$pathname$split = el.pathname.split('/'),
	            _el$pathname$split2 = _slicedToArray(_el$pathname$split, 4),
	            kind = _el$pathname$split2[2],
	            step = _el$pathname$split2[3];

	        tasks.resetCreate();
	        tasks.updateCreateRoute({ kind: kind, step: step });
	    },
	    'submit .create--subject-create form': function submitCreateSubjectCreateForm(e, el) {
	        if (e) e.preventDefault();
	        var values = getFormValues(el);
	        values = parseFormValues(values);
	        var errors = tasks.validateForm(values, subjectSchema, ['name', 'language', 'body', 'members']);
	        if (errors && errors.length) {
	            return;
	        }
	        var data = {
	            topic: {
	                name: 'Create a Subject: ' + values.name,
	                entity_id: '1rk0jS5EGEavSG4NBxRvPkZf',
	                entity_kind: 'unit'
	            },
	            post: {
	                kind: 'proposal',
	                body: 'Create a Subject: ' + values.name
	            },
	            subject: {
	                name: values.name,
	                body: values.body,
	                members: values.members
	            }
	        };
	        tasks.createSubjectProposal(data);
	    },
	    'submit .create--unit-create form': function submitCreateUnitCreateForm(e, el) {
	        if (e) e.preventDefault();
	        var values = getFormValues(el);
	        values = parseFormValues(values);
	        values.require_ids = values.require_ids && values.require_ids.map(function (rmap) {
	            return rmap.id;
	        }) || [];
	        var errors = tasks.validateForm(values, unitSchema, ['name', 'language', 'body', 'require_ids']);
	        if (errors && errors.length) {
	            return;
	        }
	        tasks.addMemberToAddUnits(values);
	        tasks.route('/create/unit/list');
	    },
	    'submit .create--subject-add__form': function submitCreateSubjectAdd__form(e, el) {
	        if (e) e.preventDefault();
	        var q = el.querySelector('input').value;
	        tasks.search({ q: q, kind: 'unit,subject' });
	    },
	    'submit .create--unit-add__form': function submitCreateUnitAdd__form(e, el) {
	        if (e) e.preventDefault();
	        var q = el.querySelector('input').value;
	        tasks.search({ q: q, kind: 'unit' });
	    },
	    'click .create--subject-add__add': function clickCreateSubjectAdd__add(e, el) {
	        if (e) e.preventDefault();
	        var _el$dataset = el.dataset,
	            kind = _el$dataset.kind,
	            id = _el$dataset.id,
	            name = _el$dataset.name,
	            body = _el$dataset.body;

	        tasks.addMemberToCreateSubject({ kind: kind, id: id, name: name, body: body });
	    },
	    'click .create--unit-add__add': function clickCreateUnitAdd__add(e, el) {
	        if (e) e.preventDefault();
	        var _el$dataset2 = el.dataset,
	            id = _el$dataset2.id,
	            name = _el$dataset2.name,
	            body = _el$dataset2.body,
	            version = _el$dataset2.version;

	        tasks.addMemberToAddUnits({ id: id, name: name, body: body, version: version });
	    },
	    'click .create--subject-create .form-field--entities__a': function clickCreateSubjectCreateFormFieldEntities__a(e, el) {
	        if (e) e.preventDefault();
	        var form = closest(el, 'form');
	        var values = getFormValues(form);
	        tasks.createSubjectData(values);
	        tasks.route('/create/subject/add');
	    },
	    'click .create--unit-create .form-field--entities__a': function clickCreateUnitCreateFormFieldEntities__a(e, el) {
	        if (e) e.preventDefault();
	        var form = closest(el, 'form');
	        var values = getFormValues(form);
	        values = parseFormValues(values);
	        tasks.stowProposedUnit(values);
	        tasks.route('/create/unit/create/add');
	    },
	    'click .create--subject-create .form-field--entities__remove': function clickCreateSubjectCreateFormFieldEntities__remove(e, el) {
	        if (e) e.preventDefault();
	        var id = el.id;
	        tasks.removeMemberFromCreateSubject({ id: id });
	    },
	    'click .create--unit-find__choose': function clickCreateUnitFind__choose(e, el) {
	        if (e) e.preventDefault();
	        var _el$dataset3 = el.dataset,
	            id = _el$dataset3.id,
	            name = _el$dataset3.name;

	        tasks.createChooseSubjectForUnits({ id: id, name: name });
	    },
	    'submit .create--unit-find__form': function submitCreateUnitFind__form(e, el) {
	        if (e) e.preventDefault();
	        var q = el.querySelector('input').value;
	        tasks.search({ q: q, kind: 'subject' });
	    },
	    'click .create--card-find__choose': function clickCreateCardFind__choose(e, el) {
	        if (e) e.preventDefault();
	        var _el$dataset4 = el.dataset,
	            id = _el$dataset4.id,
	            name = _el$dataset4.name;

	        tasks.createChooseUnitForCards({ id: id, name: name });
	    },
	    'submit .create--card-find__form': function submitCreateCardFind__form(e, el) {
	        if (e) e.preventDefault();
	        var q = el.querySelector('input').value;
	        tasks.search({ q: q, kind: 'unit' });
	    },
	    'submit .create--unit-create-add__form': function submitCreateUnitCreateAdd__form(e, el) {
	        if (e) e.preventDefault();
	        var q = el.querySelector('input').value;
	        tasks.search({ q: q, kind: 'unit' });
	    },
	    'click .create--unit-create-add__add': function clickCreateUnitCreateAdd__add(e, el) {
	        if (e) e.preventDefault();
	        var _el$dataset5 = el.dataset,
	            id = _el$dataset5.id,
	            name = _el$dataset5.name,
	            body = _el$dataset5.body;

	        tasks.addRequireToProposedUnit({ id: id, name: name, body: body, kind: 'unit' });
	    },
	    'click .create--unit-list__remove': function clickCreateUnitList__remove(e, el) {
	        if (e) e.preventDefault();
	        var index = el.dataset.index;
	        tasks.removeUnitFromSubject({ index: index });
	    },
	    'click .create--unit-list__submit': function clickCreateUnitList__submit(e) {
	        if (e) e.preventDefault();
	        tasks.createUnitsProposal();
	    },
	    'click .create--card-list__remove': function clickCreateCardList__remove(e, el) {
	        if (e) e.preventDefault();
	        var index = el.dataset.index;
	        tasks.removeCardFromUnit({ index: index });
	    },
	    'click .create--card-list__submit': function clickCreateCardList__submit(e) {
	        if (e) e.preventDefault();
	        tasks.createCardsProposal();
	    },
	    'change .create--card-create [name="kind"]': function changeCreateCardCreateNameKind(e, el) {
	        var form = closest(el, 'form');
	        var values = getFormValues(form);
	        tasks.stowProposedCard(values);
	    },
	    'submit .create--card-create form': function submitCreateCardCreateForm(e, el) {
	        if (e) e.preventDefault();
	        var values = getFormValues(el);
	        values = parseFormValues(values);
	        var errors = tasks.validateForm(values, cardSchema, ['name', 'language', 'kind']);
	        if (errors && errors.length) {
	            return;
	        }
	        tasks.addMemberToAddCards(values);
	        tasks.route('/create/card/list');
	    }
	});

/***/ }
/******/ ]);