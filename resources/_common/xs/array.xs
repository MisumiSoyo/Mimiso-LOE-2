//  vector arrays can't be correctly resized

string ArrayToStringInt(int ArrayID = -1)
{
    string result = "[";
    int i = 0;
    if (xsArrayGetSize(ArrayID) > 0)
    {
        for (i = 0; < xsArrayGetSize(ArrayID) - 1)
            result = result + xsArrayGetInt(ArrayID, i) + ",";
        result = result + xsArrayGetInt(ArrayID, xsArrayGetSize(ArrayID) - 1);
    }
    result = result + "]";
    return (result);
}

string ArrayToStringFloat(int ArrayID = -1)
{
    string result = "[";
    int i = 0;
    if (xsArrayGetSize(ArrayID) > 0)
    {
        for (i = 0; < xsArrayGetSize(ArrayID) - 1)
            result = result + xsArrayGetFloat(ArrayID, i) + ",";
        result = result + xsArrayGetFloat(ArrayID, xsArrayGetSize(ArrayID) - 1);
    }
    result = result + "]";
    return (result);
}


string ArrayToStringVector(int ArrayID = -1)
{
    string result = "[";
    int i = 0;
    if (xsArrayGetSize(ArrayID) > 0)
    {
        for (i = 0; < xsArrayGetSize(ArrayID) - 1)
            result = result + xsArrayGetVector(ArrayID, i) + ",";
        result = result + xsArrayGetVector(ArrayID, xsArrayGetSize(ArrayID) - 1);
    }
    result = result + "]";
    return (result);
}


void ArraySwapValueInt(int ArrayID = -1, int p = -1, int q = -1)
{
    if ((p != -1) && (q != -1))
    {
        int temp = xsArrayGetInt(ArrayID, p);
        xsArraySetInt(ArrayID, p, xsArrayGetInt(ArrayID, q));
        xsArraySetInt(ArrayID, q, temp);
    }
}

void ArraySwapValueFloat(int ArrayID = -1, int p = -1, int q = -1)
{
    if ((p != -1) && (q != -1))
    {
        float temp = xsArrayGetInt(ArrayID, p);
        xsArraySetFloat(ArrayID, p, xsArrayGetFloat(ArrayID, q));
        xsArraySetFloat(ArrayID, q, temp);
    }
}

void ArraySwapValueVector(int ArrayID = -1, int p = -1, int q = -1)
{
    if ((p != -1) && (q != -1))
    {
        vector temp = xsArrayGetVector(ArrayID, p);
        xsArraySetVector(ArrayID, p, xsArrayGetVector(ArrayID, q));
        xsArraySetVector(ArrayID, q, temp);
    }
}


int ArrayFindInt(int ArrayID = -1, int target = -1, int start = -1, int end = -1)
{
    int i = 0;
    int l = start;
    int r = end;
    if (l == -1)
        l = 0;
    if (r == -1)
        r = xsArrayGetSize(ArrayID);
    for (i = l; < r)
        if (target == xsArrayGetInt(ArrayID, i))
            return (i);
    return (0-1);
}

int ArrayFindFloat(int ArrayID = -1, float target = -1.0)
{
    int i = 0;
    for (i = 0; < xsArrayGetSize(ArrayID))
        if (target == xsArrayGetInt(ArrayID, i))
            return (i);
    return (0-1);
}

int ArrayFindVector(int ArrayID = -1, vector target = vector(-1.0, -1.0, -1.0))
{
    int i = 0;
    for (i = 0; < xsArrayGetSize(ArrayID))
        if (target == xsArrayGetVector(ArrayID, i))
            return (i);
    return (0-1);
}


int ArrayFindIntBS(int ArrayID = -1, int target = -1)
{
    int l = 0;
    int r = xsArrayGetSize(ArrayID) - 1;

    while (l <= r)
    {
        int mid = (l + r) / 2;
        int MidValue = xsArrayGetInt(ArrayID, mid);
        if (MidValue == target)
            return (mid);
        if (MidValue < target)
            l = mid + 1;
        else
            r = mid - 1;
    }
    return (0-1);
}


void ArrayInsertInt(int ArrayID = -1, int index = 0, int value = 0)
{
    int i = 0;
    xsArrayResizeInt(ArrayID, xsArrayGetSize(ArrayID) + 1);
    for (i = xsArrayGetSize(ArrayID) - 1; > index)
        xsArraySetInt(ArrayID, i, xsArrayGetInt(ArrayID, i - 1));
    xsArraySetInt(ArrayID, index, value);
}

void ArrayInsertFloat(int ArrayID = -1, int index = 0, float value = 0.0)
{
    int i = 0;
    xsArrayResizeFloat(ArrayID, xsArrayGetSize(ArrayID) + 1);
    for (i = xsArrayGetSize(ArrayID) - 1; > index)
        xsArraySetFloat(ArrayID, i, xsArrayGetFloat(ArrayID, i - 1));
    xsArraySetFloat(ArrayID, index, value);
}

void ArrayInsertVector(int ArrayID = -1, int index = 0, vector value = vector(-1.0, -1.0, -1.0))
{
    int i = 0;
    xsArrayResizeVector(ArrayID, xsArrayGetSize(ArrayID) + 1);
    for (i = xsArrayGetSize(ArrayID) - 1; > index)
        xsArraySetVector(ArrayID, i, xsArrayGetVector(ArrayID, i - 1));
    xsArraySetVector(ArrayID, index, value);
}


void ArrayRemoveInt(int ArrayID = -1, int index = 0, bool KeepOrder = true)
{
    int ArraySize = xsArrayGetSize(ArrayID);
    if (ArraySize == 1)
    {
        xsArrayResizeInt(ArrayID, 0);
        return;
    }
    if (KeepOrder)
    {
        int i = 0;
        for (i = index; < ArraySize - 1)
            xsArraySetInt(ArrayID, i, xsArrayGetInt(ArrayID, i + 1));
    }
    else
        xsArraySetInt(ArrayID, index, xsArrayGetInt(ArrayID, ArraySize - 1));
    xsArrayResizeInt(ArrayID, ArraySize - 1);
}

void ArrayRemoveFloat(int ArrayID = -1, int index = 0, bool KeepOrder = true)
{
    int ArraySize = xsArrayGetSize(ArrayID);
    if (ArraySize == 1)
    {
        xsArrayResizeFloat(ArrayID, 0);
        return;
    }
    if (KeepOrder)
    {
        int i = 0;
        for (i = index; < ArraySize - 1)
            xsArraySetFloat(ArrayID, i, xsArrayGetFloat(ArrayID, i + 1));
    }
    else
        xsArraySetFloat(ArrayID, index, xsArrayGetFloat(ArrayID, ArraySize - 1));
    xsArrayResizeFloat(ArrayID, ArraySize - 1);
}

void ArrayRemoveVector(int ArrayID = -1, int index = 0, bool KeepOrder = true)
{
    int ArraySize = xsArrayGetSize(ArrayID);
    if (ArraySize == 1)
    {
        xsArrayResizeVector(ArrayID, 0);
        return;
    }
    if (KeepOrder)
    {
        int i = 0;
        for (i = index; < ArraySize - 1)
            xsArraySetVector(ArrayID, i, xsArrayGetVector(ArrayID, i + 1));
    }
    else
        xsArraySetVector(ArrayID, index, xsArrayGetVector(ArrayID, ArraySize - 1));
    xsArrayResizeVector(ArrayID, ArraySize - 1);
}


void ArrayPushFrontInt(int ArrayID = -1, int value = 0)
{
    if (xsArrayGetSize(ArrayID) == 0)
    {
        xsArrayResizeInt(ArrayID, 1);
        xsArraySetInt(ArrayID, 1, value);
        return;
    }
    ArrayInsertInt(ArrayID, 0, value);
}

void ArrayPushFrontFloat(int ArrayID = -1, float value = 0.0)
{
    if (xsArrayGetSize(ArrayID) == 0)
    {
        xsArrayResizeFloat(ArrayID, 1);
        xsArraySetFloat(ArrayID, 1, value);
        return;
    }
    ArrayInsertFloat(ArrayID, 0, value);
}

void ArrayPushFrontVector(int ArrayID = -1, vector value = vector(-1.0, -1.0, -1.0))
{
    if (xsArrayGetSize(ArrayID) == 0)
    {
        xsArrayResizeVector(ArrayID, 1);
        xsArraySetVector(ArrayID, 1, value);
        return;
    }
    ArrayInsertVector(ArrayID, 0, value);
}


void ArrayAppendInt(int ArrayID = -1, int value = 0)
{
    xsArrayResizeInt(ArrayID, xsArrayGetSize(ArrayID) + 1);
    xsArraySetInt(ArrayID, xsArrayGetSize(ArrayID) - 1, value);
}

void ArrayAppendFloat(int ArrayID = -1, float value = 0.0)
{
    xsArrayResizeFloat(ArrayID, xsArrayGetSize(ArrayID) + 1);
    xsArraySetFloat(ArrayID, xsArrayGetSize(ArrayID) - 1, value);
}

void ArrayAppendVector(int ArrayID = -1, vector value = vector(-1.0, -1.0, -1.0))
{
    xsArrayResizeVector(ArrayID, xsArrayGetSize(ArrayID) + 1);
    xsArraySetVector(ArrayID, xsArrayGetSize(ArrayID) - 1, value);
}

void ArrayPushBackInt(int ArrayID = -1, int value = 0)
{
    ArrayAppendInt(ArrayID, value);
}

void ArrayPushBackFloat(int ArrayID = -1, float value = 0.0)
{
    ArrayAppendFloat(ArrayID, value);
}

void ArrayPushBackVector(int ArrayID = -1, vector value = vector(-1.0, -1.0, -1.0))
{
    ArrayAppendVector(ArrayID, value);
}


void ArrayPopFrontInt(int ArrayID = -1)
{
    ArrayRemoveInt(ArrayID, 0);
}

void ArrayPopFrontFloat(int ArrayID = -1)
{
    ArrayRemoveFloat(ArrayID, 0);
}

void ArrayPopFrontVector(int ArrayID = -1)
{
    ArrayRemoveVector(ArrayID, 0);
}


void ArrayPopBackInt(int ArrayID = -1)
{
    xsArrayResizeInt(ArrayID, xsArrayGetSize(ArrayID) - 1);
}

void ArrayPopBackFloat(int ArrayID = -1)
{
    xsArrayResizeFloat(ArrayID, xsArrayGetSize(ArrayID) - 1);
}

void ArrayPopBackVector(int ArrayID = -1)
{
    xsArrayResizeVector(ArrayID, xsArrayGetSize(ArrayID) - 1);
}

//  获取数组头部元素
int ArrayFrontInt(int ArrayID = -1)
{
    return (xsArrayGetInt(ArrayID, 0));
}

int ArrayFrontFloat(int ArrayID = -1)
{
    return (xsArrayGetFloat(ArrayID, 0));
}

vector ArrayFrontVector(int ArrayID = -1)
{
    return (xsArrayGetVector(ArrayID, 0));
}

int ArrayEndInt(int ArrayID = -1)
{
    return (xsArrayGetInt(ArrayID, xsArrayGetSize(ArrayID) - 1));
}

int ArrayEndFloat(int ArrayID = -1)
{
    return (xsArrayGetFloat(ArrayID, xsArrayGetSize(ArrayID) - 1));
}

vector ArrayEndVector(int ArrayID = -1)
{
    return (xsArrayGetVector(ArrayID, xsArrayGetSize(ArrayID) - 1));
}


void ArrayIncInt(int ArrayID = -1, int index = 0, int value = -1)
{
    xsArraySetInt(ArrayID, index, xsArrayGetInt(ArrayID, index) + value);
}

void ArrayIncFloat(int ArrayID = -1, int index = 0, float value = -1.0)
{
    xsArraySetFloat(ArrayID, index, xsArrayGetFloat(ArrayID, index) + value);
}



void ArrayMulInt(int ArrayID = -1, int index = 0, int value = -1)
{
    xsArraySetInt(ArrayID, index, xsArrayGetInt(ArrayID, index) * value);
}

void ArrayMulFloat(int ArrayID = -1, int index = 0, float value = -1.0)
{
    xsArraySetFloat(ArrayID, index, xsArrayGetFloat(ArrayID, index) * value);
}


void QuickSortInt(int ArrayID = -1, int left = 0, int right = -1)
{
    int i = left;
    int j = right;
    if (right == -1)
        j = xsArrayGetSize(ArrayID) - 1;
    int mid = xsArrayGetInt(ArrayID, (i + j) / 2);

    while (true)
    {
        while (xsArrayGetInt(ArrayID, i) < mid)
            i++;
        while (xsArrayGetInt(ArrayID, j) > mid)
            j--;
        if (i <= j)
        {
            ArraySwapValueInt(ArrayID, i, j);
            i++;
            j--;
        }
        if (i > j)
            break;
    }
    if (left < j)
        QuickSortInt(ArrayID, left, j);
    if (i < right)
        QuickSortInt(ArrayID, i, right);
}


int NewMatrixInt(int sizea = 0, int sizeb = 0, int defaultValue = 0)
{
    int NewMatrixID = xsArrayCreateInt(sizea, 0);
    int i = 0;
    for (i = 0; < sizea)
        xsArraySetInt(NewMatrixID, i, xsArrayCreateInt(sizeb, defaultValue));
    return (NewMatrixID);
}

int NewMatrixFloat(int sizea = 0, int sizeb = 0, float defaultValue = 0.0)
{
    int NewMatrixID = xsArrayCreateInt(sizea, 0);
    int i = 0;
    for (i = 0; < sizea)
        xsArraySetInt(NewMatrixID, i, xsArrayCreateFloat(sizeb, defaultValue));
    return (NewMatrixID);
}

int NewMatrixVector(int sizea = 0, int sizeb = 0, vector defaultValue = vector(-1.0, -1.0, -1.0))
{
    int NewMatrixID =xsArrayCreateInt(sizea, 0);
    int i = 0;
    for (i = 0; < sizea)
        xsArraySetInt(NewMatrixID, i, xsArrayCreateVector(sizeb, defaultValue));
    return (NewMatrixID);
}


int MatrixGetInt(int MatrixID = -1, int indexa = 0, int indexb = 0)
{
    return (xsArrayGetInt(xsArrayGetInt(MatrixID, indexa), indexb));
}

float MatrixGetFloat(int MatrixID = -1, int indexa = 0, int indexb = 0)
{
    return (xsArrayGetFloat(xsArrayGetInt(MatrixID, indexa), indexb));
}

vector MatrixGetVector(int MatrixID = -1, int indexa = 0, int indexb = 0)
{
    return (xsArrayGetVector(xsArrayGetInt(MatrixID, indexa), indexb));
}


void MatrixSetInt(int MatrixID = -1, int indexa = 0, int indexb = 0, int value = 0)
{
    xsArraySetInt(xsArrayGetInt(MatrixID, indexa), indexb, value);
}

void MatrixSetFloat(int MatrixID = -1, int indexa = 0, int indexb = 0, float value = 0.0)
{
    xsArraySetFloat(xsArrayGetInt(MatrixID, indexa), indexb, value);
}

void MatrixSetVector(int MatrixID = -1, int indexa = 0, int indexb = 0, vector value = vector(-1.0, -1.0, -1.0))
{
    xsArraySetVector(xsArrayGetInt(MatrixID, indexa), indexb, value);
}


void MatrixAppendRowInt(int MatrixID = -1, int ArrayID = -1)
{
    if (ArrayID == -1)
        ArrayAppendInt(MatrixID, xsArrayCreateInt());
    else
        ArrayAppendInt(MatrixID, ArrayID);
}

void MatrixAppendRowFloat(int MatrixID = -1, int ArrayID = -1)
{
    if (ArrayID == -1)
        ArrayAppendInt(MatrixID, xsArrayCreateFloat());
    else
        ArrayAppendInt(MatrixID, ArrayID);
}

void MatrixAppendRowVector(int MatrixID = -1, int ArrayID = -1)
{
    if (ArrayID == -1)
        ArrayAppendInt(MatrixID, xsArrayCreateVector());
    else
        ArrayAppendInt(MatrixID, ArrayID);
}


void MatrixRemoveRowInt(int MatrixID = -1, int index = 0)
{
    ArrayRemoveInt(MatrixID, index);
}

void MatrixRemoveRowFloat(int MatrixID = -1, int index = 0)
{
    ArrayRemoveInt(MatrixID, index);
}

void MatrixRemoveRowVector(int MatrixID = -1, int index = 0)
{
    ArrayRemoveInt(MatrixID, index);
}


void MatrixInsertRowInt(int MatrixID = -1, int index = 0, int ArrayID = -1)
{
    ArrayInsertInt(MatrixID, index, ArrayID);
}

void MatrixInsertRowFloat(int MatrixID = -1, int index = 0, int ArrayID = -1)
{
    ArrayInsertInt(MatrixID, index, ArrayID);
}

void MatrixInsertRowVector(int MatrixID = -1, int index = 0, int ArrayID = -1)
{
    ArrayInsertInt(MatrixID, index, ArrayID);
}


string MatrixToStringInt(int MatrixID = -1)
{
    string result = "[";
    int i = 0;
    if (xsArrayGetSize(MatrixID) > 0)
    {
        for (i = 0; < xsArrayGetSize(MatrixID) - 1)
            result = result + ArrayToStringInt(xsArrayGetInt(MatrixID, i)) + ",";
        result = result + ArrayToStringInt(xsArrayGetInt(MatrixID, xsArrayGetSize(MatrixID) - 1));
    }
    result = result + "]";
    return (result);
}

string MatrixToStringFloat(int MatrixID = -1)
{
    string result = "[";
    int i = 0;
    if (xsArrayGetSize(MatrixID) > 0)
    {
        for (i = 0; < xsArrayGetSize(MatrixID) - 1)
            result = result + ArrayToStringFloat(xsArrayGetInt(MatrixID, i)) + ",";
        result = result + ArrayToStringFloat(xsArrayGetInt(MatrixID, xsArrayGetSize(MatrixID) - 1));
    }
    result = result + "]";
    return (result);
}

string MatrixToStringVector(int MatrixID = -1)
{
    string result = "[";
    int i = 0;
    if (xsArrayGetSize(MatrixID) > 0)
    {
        for (i = 0; < xsArrayGetSize(MatrixID) - 1)
            result = result + ArrayToStringVector(xsArrayGetInt(MatrixID, i)) + ",";
        result = result + ArrayToStringVector(xsArrayGetInt(MatrixID, xsArrayGetSize(MatrixID) - 1));
    }
    result = result + "]";
    return (result);
}


int MatrixFindInt(int MatrixID = -1, int row = -1, int value = -1)
{
    return (ArrayFindInt(xsArrayGetInt(MatrixID, row), value));
}

int MatrixFindFloat(int MatrixID = -1, int row = -1, float value = -1.0)
{
    return (ArrayFindFloat(xsArrayGetInt(MatrixID, row), value));
}

int MatrixFindVector(int MatrixID = -1, int row = -1, vector value = vector(-1.0, -1.0, -1.0))
{
    return (ArrayFindVector(xsArrayGetInt(MatrixID, row), value));
}


void MatrixIncInt(int MatrixID = -1, int row = -1, int column = -1 , int value = -1)
{
    ArrayIncInt(xsArrayGetInt(MatrixID, row), column, value);
}

void MatrixIncFloat(int MatrixID = -1, int row = -1, int column = -1 , float value = -1.0)
{
    ArrayIncFloat(xsArrayGetInt(MatrixID, row), column, value);
}


void MatrixMulInt(int MatrixID = -1, int row = -1, int column = -1 , int value = -1)
{
    ArrayMulInt(xsArrayGetInt(MatrixID, row), column, value);
}

void MatrixMulFloat(int MatrixID = -1, int row = -1, int column = -1 , float value = -1.0)
{
    ArrayMulFloat(xsArrayGetInt(MatrixID, row), column, value);
}


void MatrixInsertInt(int MatrixID = -1, int row = -1, int column = -1, int value = -1)
{
    ArrayInsertInt(xsArrayGetInt(MatrixID, row), column, value);
}

void MatrixInsertFloat(int MatrixID = -1, int row = -1, int column = -1, float value = -1.0)
{
    ArrayInsertFloat(xsArrayGetInt(MatrixID, row), column, value);
}

void MatrixInsertVector(int MatrixID = -1, int row = -1, int column = -1, vector value = vector(-1.0, -1.0, -1.0))
{
    ArrayInsertVector(xsArrayGetInt(MatrixID, row), column, value);
}


void MatrixAppendInt(int MatrixID = -1, int row = -1, int value = -1)
{
    ArrayAppendInt(xsArrayGetInt(MatrixID, row), value);
}

void MatrixAppendFloat(int MatrixID = -1, int row = -1, float value = -1.0)
{
    ArrayAppendFloat(xsArrayGetInt(MatrixID, row), value);
}

void MatrixAppendVector(int MatrixID = -1, int row = -1, vector value = vector(-1.0, -1.0, -1.0))
{
    ArrayAppendVector(xsArrayGetInt(MatrixID, row), value);
}


void MatrixRemoveInt(int MatrixID = -1, int row = -1, int column = -1, bool KeepOrder = true)
{
    ArrayRemoveInt(xsArrayGetInt(MatrixID, row), column, KeepOrder);
}

void MatrixRemoveFloat(int MatrixID = -1, int row = -1, int column = -1)
{
    ArrayRemoveFloat(xsArrayGetInt(MatrixID, row), column);
}

void MatrixRemoveVector(int MatrixID = -1, int row = -1, int column = -1)
{
    ArrayRemoveVector(xsArrayGetInt(MatrixID, row), column);
}


void MatrixPopFrontInt(int MatrixID = -1, int row = -1)
{
    ArrayPopFrontInt(xsArrayGetInt(MatrixID, row));
}

void MatrixPopFrontFloat(int MatrixID = -1, int row = -1)
{
    ArrayPopFrontFloat(xsArrayGetInt(MatrixID, row));
}

void MatrixPopFrontVector(int MatrixID = -1, int row = -1)
{
    ArrayPopFrontVector(xsArrayGetInt(MatrixID, row));
}


void MatrixPopBackInt(int MatrixID = -1, int row = -1)
{
    ArrayPopBackInt(xsArrayGetInt(MatrixID, row));
}

void MatrixPopBackFloat(int MatrixID = -1, int row = -1)
{
    ArrayPopBackFloat(xsArrayGetInt(MatrixID, row));
}

void MatrixPopBackVector(int MatrixID = -1, int row = -1)
{
    ArrayPopBackVector(xsArrayGetInt(MatrixID, row));
}


int MatrixRowLength(int MatrixID = -1, int row = -1)
{
    return (xsArrayGetSize(xsArrayGetInt(MatrixID, row)));
}