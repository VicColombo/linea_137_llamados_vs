
# check_array

def check_array(array, accept_sparse=False, *, accept_large_sparse=True,
                dtype="numeric", order=None, copy=False, force_all_finite=True,
                ensure_2d=True, allow_nd=False, ensure_min_samples=1,
                ensure_min_features=1, estimator=None):

    """Input validation on an array, list, sparse matrix or similar.

    By default, the input is checked to be a non-empty 2D array containing
    only finite values. If the dtype of the array is object, attempt
    converting to float, raising on failure.

    Parameters
    ----------
    array : object
        Input object to check / convert.

    accept_sparse : string, boolean or list/tuple of strings (default=False)
        String[s] representing allowed sparse matrix formats, such as 'csc',
        'csr', etc. If the input is sparse but not in the allowed format,
        it will be converted to the first listed format. True allows the input
        to be any format. False means that a sparse matrix input will
        raise an error.

    accept_large_sparse : bool (default=True)
        If a CSR, CSC, COO or BSR sparse matrix is supplied and accepted by
        accept_sparse, accept_large_sparse=False will cause it to be accepted
        only if its indices are stored with a 32-bit dtype.

        .. versionadded:: 0.20

    dtype : string, type, list of types or None (default="numeric")
        Data type of result. If None, the dtype of the input is preserved.
        If "numeric", dtype is preserved unless array.dtype is object.
        If dtype is a list of types, conversion on the first type is only
        performed if the dtype of the input is not in the list.

    order : 'F', 'C' or None (default=None)
        Whether an array will be forced to be fortran or c-style.
        When order is None (default), then if copy=False, nothing is ensured
        about the memory layout of the output array; otherwise (copy=True)
        the memory layout of the returned array is kept as close as possible
        to the original array.

    copy : boolean (default=False)
        Whether a forced copy will be triggered. If copy=False, a copy might
        be triggered by a conversion.

    force_all_finite : boolean or 'allow-nan', (default=True)
        Whether to raise an error on np.inf, np.nan, pd.NA in array. The
        possibilities are:

        - True: Force all values of array to be finite.
        - False: accepts np.inf, np.nan, pd.NA in array.
        - 'allow-nan': accepts only np.nan and pd.NA values in array. Values
          cannot be infinite.

        .. versionadded:: 0.20
           ``force_all_finite`` accepts the string ``'allow-nan'``.

        .. versionchanged:: 0.23
           Accepts `pd.NA` and converts it into `np.nan`

    ensure_2d : boolean (default=True)
        Whether to raise a value error if array is not 2D.

    allow_nd : boolean (default=False)
        Whether to allow array.ndim > 2.

    ensure_min_samples : int (default=1)
        Make sure that the array has a minimum number of samples in its first
        axis (rows for a 2D array). Setting to 0 disables this check.

    ensure_min_features : int (default=1)
        Make sure that the 2D array has some minimum number of features
        (columns). The default value of 1 rejects empty datasets.
        This check is only enforced when the input data has effectively 2
        dimensions or is originally 1D and ``ensure_2d`` is True. Setting to 0
        disables this check.

    estimator : str or estimator instance (default=None)
        If passed, include the name of the estimator in warning messages.

    Returns
    -------
    array_converted : object
        The converted and validated array.
    """
    # store reference to original array to check if copy is needed when
    # function returns
    array_orig = array

    # store whether originally we wanted numeric dtype
    dtype_numeric = isinstance(dtype, str) and dtype == "numeric"

    dtype_orig = getattr(array, "dtype", None)
    if not hasattr(dtype_orig, 'kind'):
        # not a data type (e.g. a column named dtype in a pandas DataFrame)
        dtype_orig = None

    # check if the object contains several dtypes (typically a pandas
    # DataFrame), and store them. If not, store None.
    dtypes_orig = None
    has_pd_integer_array = False
    if hasattr(array, "dtypes") and hasattr(array.dtypes, '__array__'):
        # throw warning if columns are sparse. If all columns are sparse, then
        # array.sparse exists and sparsity will be perserved (later).
        with suppress(ImportError):
            from pandas.api.types import is_sparse
            if (not hasattr(array, 'sparse') and
                    array.dtypes.apply(is_sparse).any()):
                warnings.warn(
                    "pandas.DataFrame with sparse columns found."
                    "It will be converted to a dense numpy array."
                )

        dtypes_orig = list(array.dtypes)
        # pandas boolean dtype __array__ interface coerces bools to objects
        for i, dtype_iter in enumerate(dtypes_orig):
            if dtype_iter.kind == 'b':
                dtypes_orig[i] = np.dtype(np.object)
            elif dtype_iter.name.startswith(("Int", "UInt")):
                # name looks like an Integer Extension Array, now check for
                # the dtype
                with suppress(ImportError):
                    from pandas import (Int8Dtype, Int16Dtype,
                                        Int32Dtype, Int64Dtype,
                                        UInt8Dtype, UInt16Dtype,
                                        UInt32Dtype, UInt64Dtype)
                    if isinstance(dtype_iter, (Int8Dtype, Int16Dtype,
                                               Int32Dtype, Int64Dtype,
                                               UInt8Dtype, UInt16Dtype,
                                               UInt32Dtype, UInt64Dtype)):
                        has_pd_integer_array = True

        if all(isinstance(dtype, np.dtype) for dtype in dtypes_orig):
            dtype_orig = np.result_type(*dtypes_orig)

    if dtype_numeric:
        if dtype_orig is not None and dtype_orig.kind == "O":
            # if input is object, convert to float.
            dtype = np.float64
        else:
            dtype = None

    if isinstance(dtype, (list, tuple)):
        if dtype_orig is not None and dtype_orig in dtype:
            # no dtype conversion required
            dtype = None
        else:
            # dtype conversion required. Let's select the first element of the
            # list of accepted types.
            dtype = dtype[0]

    if has_pd_integer_array:
        # If there are any pandas integer extension arrays,
        array = array.astype(dtype)

    if force_all_finite not in (True, False, 'allow-nan'):
        raise ValueError('force_all_finite should be a bool or "allow-nan"'
                         '. Got {!r} instead'.format(force_all_finite))

    if estimator is not None:
        if isinstance(estimator, str):
            estimator_name = estimator
        else:
            estimator_name = estimator.__class__.__name__
    else:
        estimator_name = "Estimator"
    context = " by %s" % estimator_name if estimator is not None else ""

    # When all dataframe columns are sparse, convert to a sparse array
    if hasattr(array, 'sparse') and array.ndim > 1:
        # DataFrame.sparse only supports `to_coo`
        array = array.sparse.to_coo()

    if sp.issparse(array):
        _ensure_no_complex_data(array)
        array = _ensure_sparse_format(array, accept_sparse=accept_sparse,
                                      dtype=dtype, copy=copy,
                                      force_all_finite=force_all_finite,
                                      accept_large_sparse=accept_large_sparse)
    else:
        # If np.array(..) gives ComplexWarning, then we convert the warning
        # to an error. This is needed because specifying a non complex
        # dtype to the function converts complex to real dtype,
        # thereby passing the test made in the lines following the scope
        # of warnings context manager.
        with warnings.catch_warnings():
            try:
                warnings.simplefilter('error', ComplexWarning)
                if dtype is not None and np.dtype(dtype).kind in 'iu':
                    # Conversion float -> int should not contain NaN or
                    # inf (numpy#14412). We cannot use casting='safe' because
                    # then conversion float -> int would be disallowed.
                    array = np.asarray(array, order=order)
                    if array.dtype.kind == 'f':
                        _assert_all_finite(array, allow_nan=False,
                                           msg_dtype=dtype)
                    array = array.astype(dtype, casting="unsafe", copy=False)
                else:
                    array = np.asarray(array, order=order, dtype=dtype)
            except ComplexWarning:
                raise ValueError("Complex data not supported\n"
                                 "{}\n".format(array))

        # It is possible that the np.array(..) gave no warning. This happens
        # when no dtype conversion happened, for example dtype = None. The
        # result is that np.array(..) produces an array of complex dtype
        # and we need to catch and raise exception for such cases.
        _ensure_no_complex_data(array)

        if ensure_2d:
            # If input is scalar raise error
            if array.ndim == 0:
                raise ValueError(
                    "Expected 2D array, got scalar array instead:\narray={}.\n"
                    "Reshape your data either using array.reshape(-1, 1) if "
                    "your data has a single feature or array.reshape(1, -1) "
                    "if it contains a single sample.".format(array))
            # If input is 1D raise error
            if array.ndim == 1:
                raise ValueError(
                    "Expected 2D array, got 1D array instead:\narray={}.\n"
                    "Reshape your data either using array.reshape(-1, 1) if "
                    "your data has a single feature or array.reshape(1, -1) "
                    "if it contains a single sample.".format(array))

        # in the future np.flexible dtypes will be handled like object dtypes
        if dtype_numeric and np.issubdtype(array.dtype, np.flexible):
            warnings.warn(
                "Beginning in version 0.22, arrays of bytes/strings will be "
                "converted to decimal numbers if dtype='numeric'. "
                "It is recommended that you convert the array to "
                "a float dtype before using it in scikit-learn, "
                "for example by using "
                "your_array = your_array.astype(np.float64).",
                FutureWarning, stacklevel=2)

        # make sure we actually converted to numeric:
        if dtype_numeric and array.dtype.kind == "O":
            array = array.astype(np.float64)
        if not allow_nd and array.ndim >= 3:
            raise ValueError("Found array with dim %d. %s expected <= 2."
                             % (array.ndim, estimator_name))

        if force_all_finite:
            _assert_all_finite(array,
                               allow_nan=force_all_finite == 'allow-nan')

    if ensure_min_samples > 0:
        n_samples = _num_samples(array)
        if n_samples < ensure_min_samples:
            raise ValueError("Found array with %d sample(s) (shape=%s) while a"
                             " minimum of %d is required%s."
                             % (n_samples, array.shape, ensure_min_samples,
                                context))

    if ensure_min_features > 0 and array.ndim == 2:
        n_features = array.shape[1]
        if n_features < ensure_min_features:
            raise ValueError("Found array with %d feature(s) (shape=%s) while"
                             " a minimum of %d is required%s."
                             % (n_features, array.shape, ensure_min_features,
                                context))

    if copy and np.may_share_memory(array, array_orig):
        array = np.array(array, dtype=dtype, order=order)

    return array



# _array_indexing

def _array_indexing(array, key, key_dtype, axis, complement):
    """Index an array or scipy.sparse consistently across NumPy version."""
    if issparse(array):
        # check if we have an boolean array-likes to make the proper indexing
        if key_dtype == 'bool':
            key = np.asarray(key)
    if isinstance(key, tuple):
        key = list(key)
    if complement:
        mask = np.ones(array.shape[0] if axis == 0 else array.shape[1], bool)
        mask[key] = False
        key = mask
    return array[key] if axis == 0 else array[:, key]







# _pandas_indexing

def _pandas_indexing(X, key, key_dtype, axis, complement):
    """Index a pandas dataframe or a series."""
    if hasattr(key, 'shape'):
        # Work-around for indexing with read-only key in pandas
        # FIXME: solved in pandas 0.25
        key = np.asarray(key)
        key = key if key.flags.writeable else key.copy()
    elif isinstance(key, tuple):
        key = list(key)
    # check whether we should index with loc or iloc
    indexer = X.iloc if key_dtype == 'int' else X.loc
    if complement:
        if key_dtype == 'str':
            # we reject string keys for rows
            key = _get_column_indices(X, key)
        if isinstance(key, tuple):
            key = list(key)
        mask = np.ones(X.shape[0] if axis == 0 else X.shape[1], bool)
        mask[key] = False
        key = mask
    return indexer[:, key] if axis else indexer[key]



# _list_indexing

def _list_indexing(X, key, key_dtype, complement):
    """Index a Python list."""
    if complement:
        if isinstance(key, tuple):
            key = list(key)
        mask = np.ones(len(X), bool)
        mask[key] = False
        key = mask
        key_dtype = 'bool'

    if np.isscalar(key) or isinstance(key, slice):
        # key is a slice or a scalar
        return X[key]
    if key_dtype == 'bool':
        # key is a boolean array-like
        return list(compress(X, key))
    # key is a integer array-like of key
    return [X[idx] for idx in key]


# _determine_key_type


def _determine_key_type(key, accept_slice=True):
    """Determine the data type of key.

    Parameters
    ----------
    key : scalar, slice or array-like
        The key from which we want to infer the data type.

    accept_slice : bool, default=True
        Whether or not to raise an error if the key is a slice.

    Returns
    -------
    dtype : {'int', 'str', 'bool', None}
        Returns the data type of key.
    """
    err_msg = ("No valid specification of the columns. Only a scalar, list or "
               "slice of all integers or all strings, or boolean mask is "
               "allowed")

    dtype_to_str = {int: 'int', str: 'str', bool: 'bool', np.bool_: 'bool'}
    array_dtype_to_str = {'i': 'int', 'u': 'int', 'b': 'bool', 'O': 'str',
                          'U': 'str', 'S': 'str'}

    if key is None:
        return None
    if isinstance(key, tuple(dtype_to_str.keys())):
        try:
            return dtype_to_str[type(key)]
        except KeyError:
            raise ValueError(err_msg)
    if isinstance(key, slice):
        if not accept_slice:
            raise TypeError(
                'Only array-like or scalar are supported. '
                'A Python slice was given.'
            )
        if key.start is None and key.stop is None:
            return None
        key_start_type = _determine_key_type(key.start)
        key_stop_type = _determine_key_type(key.stop)
        if key_start_type is not None and key_stop_type is not None:
            if key_start_type != key_stop_type:
                raise ValueError(err_msg)
        if key_start_type is not None:
            return key_start_type
        return key_stop_type
    if isinstance(key, (list, tuple)):
        unique_key = set(key)
        key_type = {_determine_key_type(elt) for elt in unique_key}
        if not key_type:
            return None
        if len(key_type) != 1:
            raise ValueError(err_msg)
        return key_type.pop()
    if hasattr(key, 'dtype'):
        try:
            return array_dtype_to_str[key.dtype.kind]
        except KeyError:
            raise ValueError(err_msg)
    raise ValueError(err_msg)








# _safe_indexing



def _safe_indexing(X, indices, *, axis=0, complement=False):
    """Return rows, items or columns of X using indices.

    .. warning::

        This utility is documented, but **private**. This means that
        backward compatibility might be broken without any deprecation
        cycle.

    Parameters
    ----------
    X : array-like, sparse-matrix, list, pandas.DataFrame, pandas.Series
        Data from which to sample rows, items or columns. `list` are only
        supported when `axis=0`.
    indices : bool, int, str, slice, array-like
        - If `axis=0`, boolean and integer array-like, integer slice,
          and scalar integer are supported.
        - If `axis=1`:
            - to select a single column, `indices` can be of `int` type for
              all `X` types and `str` only for dataframe. The selected subset
              will be 1D, unless `X` is a sparse matrix in which case it will
              be 2D.
            - to select multiples columns, `indices` can be one of the
              following: `list`, `array`, `slice`. The type used in
              these containers can be one of the following: `int`, 'bool' and
              `str`. However, `str` is only supported when `X` is a dataframe.
              The selected subset will be 2D.
    axis : int, default=0
        The axis along which `X` will be subsampled. `axis=0` will select
        rows while `axis=1` will select columns.
    complement : bool, default=False
        Whether to select the given columns or deselect them and return the
        rest.

    Returns
    -------
    subset
        Subset of X on axis 0 or 1.

    Notes
    -----
    CSR, CSC, and LIL sparse matrices are supported. COO sparse matrices are
    not supported.
    """
    if indices is None:
        return X

    if axis not in (0, 1):
        raise ValueError(
            "'axis' should be either 0 (to index rows) or 1 (to index "
            " column). Got {} instead.".format(axis)
        )

    indices_dtype = _determine_key_type(indices)

    if axis == 0 and indices_dtype == 'str':
        raise ValueError(
            "String indexing is not supported with 'axis=0'"
        )

    if axis == 1 and X.ndim != 2:
        raise ValueError(
            "'X' should be a 2D NumPy array, 2D sparse matrix or pandas "
            "dataframe when indexing the columns (i.e. 'axis=1'). "
            "Got {} instead with {} dimension(s).".format(type(X), X.ndim)
        )

    if axis == 1 and indices_dtype == 'str' and not hasattr(X, 'loc'):
        raise ValueError(
            "Specifying the columns using strings is only supported for "
            "pandas DataFrames"
        )

    if hasattr(X, "iloc"):
        return _pandas_indexing(X, indices, indices_dtype, axis=axis,
                                complement=complement)
    elif hasattr(X, "shape"):
        return _array_indexing(X, indices, indices_dtype, axis=axis,
                               complement=complement)
    else:
        return _list_indexing(X, indices, indices_dtype,
                              complement=complement)







# _get_column_indices

def _get_column_indices(X, key):
    """Get feature column indices for input data X and key.

    For accepted values of `key`, see the docstring of
    :func:`_safe_indexing_column`.
    """
    n_columns = X.shape[1]

    key_dtype = _determine_key_type(key)

    if isinstance(key, (list, tuple)) and not key:
        # we get an empty list
        return []
    elif key_dtype in ('bool', 'int'):
        # Convert key into positive indexes
        try:
            idx = _safe_indexing(np.arange(n_columns), key)
        except IndexError as e:
            raise ValueError(
                'all features must be in [0, {}] or [-{}, 0]'
                .format(n_columns - 1, n_columns)
            ) from e
        return np.atleast_1d(idx).tolist()
    elif key_dtype == 'str':
        try:
            all_columns = X.columns
        except AttributeError:
            raise ValueError("Specifying the columns using strings is only "
                             "supported for pandas DataFrames")
        if isinstance(key, str):
            columns = [key]
        elif isinstance(key, slice):
            start, stop = key.start, key.stop
            if start is not None:
                start = all_columns.get_loc(start)
            if stop is not None:
                # pandas indexing with strings is endpoint included
                stop = all_columns.get_loc(stop) + 1
            else:
                stop = n_columns + 1
            return list(range(n_columns)[slice(start, stop)])
        else:
            columns = list(key)

        try:
            column_indices = []
            for col in columns:
                col_idx = all_columns.get_loc(col)
                if not isinstance(col_idx, numbers.Integral):
                    raise ValueError(f"Selected columns, {columns}, are not "
                                     "unique in dataframe")
                column_indices.append(col_idx)

        except KeyError as e:
            raise ValueError(
                "A given column is not a column of the dataframe"
            ) from e

        return column_indices
    else:
        raise ValueError("No valid specification of the columns. Only a "
                         "scalar, list or slice of all integers or all "
                         "strings, or boolean mask is allowed")






# _split_categorical_numerical

def _split_categorical_numerical(X, categorical_features):
    # the following bit is done before check_pairwise_array to avoid converting
    # numerical data to object dtype. First we split the data into categorical
    # and numerical, then we do check_array

    if X is None:
        return None, None

    # TODO: this should be more like check_array(..., accept_pandas=True)
    if not hasattr(X, "shape"):
        X = check_array(X, dtype=np.object, force_all_finite=False)

    cols = categorical_features
    if cols is None:
        cols = []

    col_idx = _get_column_indices(X, cols)
    X_cat = _safe_indexing(X, col_idx, axis=1)
    X_num = _safe_indexing(X, col_idx, axis=1, complement=True)

    return X_cat, X_num






# _return_float_dtype

def _return_float_dtype(X, Y):
    """
    1. If dtype of X and Y is float32, then dtype float32 is returned.
    2. Else dtype float is returned.
    """
    if not issparse(X) and not isinstance(X, np.ndarray):
        X = np.asarray(X)

    if Y is None:
        Y_dtype = X.dtype
    elif not issparse(Y) and not isinstance(Y, np.ndarray):
        Y = np.asarray(Y)
        Y_dtype = Y.dtype
    else:
        Y_dtype = Y.dtype

    if X.dtype == Y_dtype == np.float32:
        dtype = np.float32
    else:
        dtype = np.float

    return X, Y, dtype






# check_pairwise_arrays

def check_pairwise_arrays(X, Y, *, precomputed=False, dtype=None,
                          accept_sparse='csr', force_all_finite=True,
                          copy=False):
    """ Set X and Y appropriately and checks inputs

    If Y is None, it is set as a pointer to X (i.e. not a copy).
    If Y is given, this does not happen.
    All distance metrics should use this function first to assert that the
    given parameters are correct and safe to use.

    Specifically, this function first ensures that both X and Y are arrays,
    then checks that they are at least two dimensional while ensuring that
    their elements are floats (or dtype if provided). Finally, the function
    checks that the size of the second dimension of the two arrays is equal, or
    the equivalent check for a precomputed distance matrix.

    Parameters
    ----------
    X : {array-like, sparse matrix}, shape (n_samples_a, n_features)

    Y : {array-like, sparse matrix}, shape (n_samples_b, n_features)

    precomputed : bool
        True if X is to be treated as precomputed distances to the samples in
        Y.

    dtype : string, type, list of types or None (default=None)
        Data type required for X and Y. If None, the dtype will be an
        appropriate float type selected by _return_float_dtype.

        .. versionadded:: 0.18

    accept_sparse : string, boolean or list/tuple of strings
        String[s] representing allowed sparse matrix formats, such as 'csc',
        'csr', etc. If the input is sparse but not in the allowed format,
        it will be converted to the first listed format. True allows the input
        to be any format. False means that a sparse matrix input will
        raise an error.

    force_all_finite : boolean or 'allow-nan', (default=True)
        Whether to raise an error on np.inf, np.nan, pd.NA in array. The
        possibilities are:

        - True: Force all values of array to be finite.
        - False: accepts np.inf, np.nan, pd.NA in array.
        - 'allow-nan': accepts only np.nan and pd.NA values in array. Values
          cannot be infinite.

        .. versionadded:: 0.22
           ``force_all_finite`` accepts the string ``'allow-nan'``.

        .. versionchanged:: 0.23
           Accepts `pd.NA` and converts it into `np.nan`

    copy : bool
        Whether a forced copy will be triggered. If copy=False, a copy might
        be triggered by a conversion.

        .. versionadded:: 0.22

    Returns
    -------
    safe_X : {array-like, sparse matrix}, shape (n_samples_a, n_features)
        An array equal to X, guaranteed to be a numpy array.

    safe_Y : {array-like, sparse matrix}, shape (n_samples_b, n_features)
        An array equal to Y if Y was not None, guaranteed to be a numpy array.
        If Y was None, safe_Y will be a pointer to X.

    """
    X, Y, dtype_float = _return_float_dtype(X, Y)

    estimator = 'check_pairwise_arrays'
    if dtype is None:
        dtype = dtype_float

    if Y is X or Y is None:
        X = Y = check_array(X, accept_sparse=accept_sparse, dtype=dtype,
                            copy=copy, force_all_finite=force_all_finite,
                            estimator=estimator)
    else:
        X = check_array(X, accept_sparse=accept_sparse, dtype=dtype,
                        copy=copy, force_all_finite=force_all_finite,
                        estimator=estimator)
        Y = check_array(Y, accept_sparse=accept_sparse, dtype=dtype,
                        copy=copy, force_all_finite=force_all_finite,
                        estimator=estimator)

    if precomputed:
        if X.shape[1] != Y.shape[0]:
            raise ValueError("Precomputed metric requires shape "
                             "(n_queries, n_indexed). Got (%d, %d) "
                             "for %d indexed." %
                             (X.shape[0], X.shape[1], Y.shape[0]))
    elif X.shape[1] != Y.shape[1]:
        raise ValueError("Incompatible dimension for X and Y matrices: "
                         "X.shape[1] == %d while Y.shape[1] == %d" % (
                             X.shape[1], Y.shape[1]))

    return X, Y






# gower distance
def gower_distances(X, Y=None, categorical_features=None, scale=True,
                    min_values=None, scale_factor=None):
    """Compute the distances between the observations in X and Y,
    that may contain mixed types of data, using an implementation
    of Gower formula.

    Parameters
    ----------
    X : {array-like, pandas.DataFrame} of shape (n_samples, n_features)

    Y : {array-like, pandas.DataFrame} of shape (n_samples, n_features), \
        default=None

    categorical_features : array-like of str, array-like of int, \
            array-like of bool, slice or callable, default=None
        Indexes the data on its second axis. Integers are interpreted as
        positional columns, while strings can reference DataFrame columns
        by name.
        A callable is passed the input data `X` and can return any of the
        above. To select multiple columns by name or dtype, you can use
        :obj:`~sklearn.compose.make_column_selector`.

        By default all non-numeric columns are considered categorical.

    scale : bool, default=True
        Indicates if the numerical columns should be scaled to [0, 1].
        If ``False``, the numerical columns are assumed to be already scaled.
        The scaling factors, _i.e._ ``min_values`` and ``scale_factor``, are
        taken from ``X``. If ``X`` and ``Y`` are both provided, ``min_values``
        and ``scale_factor`` have to be provided as well.

    min_values : ndarray of shape (n_features,), default=None
        Per feature adjustment for minimum. Equivalent to
        ``min_values - X.min(axis=0) * scale_factor``
        If provided, ``scale_factor`` should be provided as well.
        Only relevant if ``scale=True``.

    scale_factor : ndarray of shape (n_features,), default=None
        Per feature relative scaling of the data. Equivalent to
        ``(max_values - min_values) / (X.max(axis=0) - X.min(axis=0))``
        If provided, ``min_values`` should be provided as well.
        Only relevant if ``scale=True``.

    Returns
    -------
    distances : ndarray of shape (n_samples_X, n_samples_Y)

    References
    ----------
    Gower, J.C., 1971, A General Coefficient of Similarity and Some of Its
    Properties.

    Notes
    -----
    Categorical ordinal attributes should be treated as numeric for the purpose
    of Gower similarity.

    Current implementation does not support sparse matrices.

    This implementation modifies the Gower's original similarity measure in
    the sense that this implementation returns 1-S.
    """
    def _nanmanhatan(x, y):
        return np.nansum(np.abs(x - y))

    def _non_nans(x, y):
        return len(x) - np.sum(_object_dtype_isnan(x) | _object_dtype_isnan(y))

    def _nanhamming(x, y):
        return np.sum(x != y) - np.sum(
            _object_dtype_isnan(x) | _object_dtype_isnan(y))

    if issparse(X) or issparse(Y):
        raise TypeError("Gower distance does not support sparse matrices")

    if X is None or len(X) == 0:
        raise ValueError("X can not be None or empty")

    if scale:
        if (scale_factor is None) != (min_values is None):
            raise ValueError("min_value and scale_factor should be provided "
                             "together.")

    # scale_factor and min_values are either both None or not at this point
    if X is not Y and Y is not None and scale_factor is None and scale:
        raise ValueError("`scaling_factor` and `min_values` must be provided "
                         "when `Y` is provided and `scale=True`")

    if callable(categorical_features):
        cols = categorical_features(X)
    else:
        cols = categorical_features
    X_cat, X_num = _split_categorical_numerical(X, categorical_features=cols)
    Y_cat, Y_num = _split_categorical_numerical(Y, categorical_features=cols)

    if min_values is not None:
        min_values = np.asarray(min_values)
        scale_factor = np.asarray(scale_factor)
        check_consistent_length(min_values, scale_factor,
                                np.ndarray(shape=(X_num.shape[1], 0)))

    if X_num.shape[1]:
        X_num, Y_num = check_pairwise_arrays(X_num, Y_num, precomputed=False,
                                             dtype=float,
                                             force_all_finite=False)
        if scale:
            scale_data = X_num if Y_num is X_num else np.vstack((X_num, Y_num))
            if scale_factor is None:
                trs = MinMaxScaler().fit(scale_data)
            else:
                trs = MinMaxScaler()
                trs.scale_ = scale_factor
                trs.min_ = min_values
            X_num = trs.transform(X_num)
            Y_num = trs.transform(Y_num)

        nan_manhatan = distance.cdist(X_num, Y_num, _nanmanhatan)
        # nan_manhatan = np.nansum(np.abs(X_num - Y_num))
        valid_num = distance.cdist(X_num, Y_num, _non_nans)
    else:
        nan_manhatan = valid_num = None

    if X_cat.shape[1]:
        X_cat, Y_cat = check_pairwise_arrays(X_cat, Y_cat, precomputed=False,
                                             dtype=np.object,
                                             force_all_finite=False)
        nan_hamming = distance.cdist(X_cat, Y_cat, _nanhamming)
        valid_cat = distance.cdist(X_cat, Y_cat, _non_nans)
    else:
        nan_hamming = valid_cat = None

    # based on whether there are categorical and/or numerical data present,
    # we compute the distance metric
    # Division by zero and nans warnings are ignored since they are expected
    with np.errstate(divide='ignore', invalid='ignore'):
        if valid_num is not None and valid_cat is not None:
            D = (nan_manhatan + nan_hamming) / (valid_num + valid_cat)
        elif valid_num is not None:
            D = nan_manhatan / valid_num
        else:
            D = nan_hamming / valid_cat
    return D
