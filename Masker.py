# Python 2x & PIL required

from PIL import Image
from copy import deepcopy
# ������� ��������� �����������: �������� � ������, � ��� ��� ��������;
#  ��� ������� ����������� �������� ����� ������ �� ������� ��������.
from time import ctime, time as now

def mask (img, condition=None):
    '''
  ������ ������� ������������� ����������� � ������ �����,
� ������� ������� ����������� �� ������� "condition" �������
�������������� �������, � ������� ������������� - ����.
    '''
    matrix = []
    # ���������� matrix ��������� ������� �����, ������ ������ � �����.
    pixels = 0
    # ���������� pixels ��������� ����� ���������� ������������ ��������
    approved = 0
    # ���������� approved ��������� ���������� "����������" ��������.
    pix = img.convert('L').load()
    for j in range(img.size[1]):
        matrix.append([])
        # ��� ������ ������� ����������� ���������������� ������ ������.
        for i in range(img.size[0]):
            pixels += 1
            # ������� ������ ����� ��������.
            '''
            if (
                (condition != None and pix[i,j] == condition) or
                (condition == None and pix[i,j])):
                # �����������, ���� ������� ������������� �������
                #  ��� �� �� ���� (�� ������) ��� ���������� �������.
                # ������, ���� ������� ����� (0, 0, 0) � RGB, �� �� ����
                matrix[j].append(1)
                # � ������� ����� ��������� �������������� �������.
                approved += 1
                # ������� "����������" ��������, ��������� ��������.
            else:
                matrix[j].append(0)
                # ���� ���� �������, �������� ������� �� �������������
                #  ��� �� ������� ������ (������, ����� "0").
            '''
            matrix[j].append(pix[i,j])
            if pix[i,j]: approved += 1
    return matrix, (pixels, approved)
    # ������� ���������� ������� �����,
    #  � ��� �� ������ (����� ��������, "����������" ��������).

def _compare (A, B=(0, 0)):
    '''
  ������ ������� ���������� ��� ������� ����������� �����.
� ���� ��������� ����� ������� ������������� ��������������,
�������������� � ���� (W, H), ��� W � H - ������ � ������ ��������������
    '''
    if (A[0]*A[1] > B[0]*B[1] or
        (A[0]*A[1] == B[0]*B[1] and
         A[0]+A[1] <= B[0]+B[1])):
        return True
        # ������� ���������� ������, ����:
        # - ������� ������� �������������� ������ ������� �������;
        # - ������� �����, �� �������� ������� �������������� ������.
    else: return False
    # �������� ��� ���:
    # - ������ ������������� ������ -�������- �� ���������������;
    # -  ����  ������������� ������ =�������= �� ���������������;
    #  �� ��������������� 2�4 (S=8) � 3�3 (S=9) ����� ������ 3�3.
    #  �� 2�6 (S=12, P=8) � 3�4 (S=12, P=7) ����� ������ 3�4.
    #  �� ��������������� 2�3 � 3�2 ����� ������ 2�3. ������ �� � ���?

def cover (matrix):
    '''
  ������ ������� ���������� ���������� ������� ��� ���������,
������������ � ������ �����. ����� �� �������� �������� ����������,
������������ ��������� ���� �������� _compare.
    '''
    result = deepcopy(matrix)
    # �������� ������ ����� �����, ����� ���
    #  �������������� ��������� ��� ���� ������,
    #  � �� ��� ���������� �����.
    width = len(matrix[0])
    height = len(matrix)
    # ��� ����������� �������� ����� ����� ������ �����.
    # �.�. ����� �������������, ����� ������ ������ ����� � �����.
    for j in range(height):
        for i in range(width):
            rectangle = (0, 0)
            colour = matrix[j][i]
            # ���������������� ������������� ������� ��������.
            if colour and matrix[j][i] == colour:
                # ����������� ������ ��� ����� � ��������,
                #  ������ � ���� ������������.
                m, n = i, j
                # ���������������� ������ ���� ��������������.
                current = []
                # ���������� current ��������� ������ ���������
                #  ��������, ����������� ���: ����� �������� - ������,
                #  �������� �������� - ������.
                max_len = width
                # ���������� max_len ������ ������������� �����,
                #  ����� �� ��������� ������ �������. (��. ������)
                
                while (m < width  and
                       n < height and
                       matrix[n][m] == colour ):
                    # ���� ��������� ��������� �����. ��� �����������,
                    #  ���� ����� ������� ���� ������ ������ �������.
                    current.append(0)
                    # ��� ����� ��������������� ������ �������� ������.
                    for l in range(max_len):
                        # ���� ��������� ������������ ������ ������.
                        if (m < width and
                            matrix[n][m] == colour ):
                            # ���� ��������������� ������������������
                            #  �� ������ � ���� ����� ��� ������ ������
                            current[n-j] += 1
                            # ������ ������������� � ������ ��������.
                            m += 1
                            # ������� � ���������� �������.
                        else:
                            max_len = l
                            # ����� ����, l ������ >= max_len,
                            #  ��� ��� max_len �� �������������,
                            #  �� ����� ����������� (��� ��������).
                            m = i
                            # ��� ������������������ ����������,
                            #  ����� �������� ���������� �� X.
                            break
                    else: m = i
                    # ���� �� ������������������ �������� ������������
                    #  �����, ������ ���� �� ����� ������.
                    # ����� �������� ����������, ������ ��� �����
                    #  �� ���������, ��� �� ��� ������ ������ �������.
                    n += 1
                    # ������� �� ��������� ������ � � ��������� ��������
                    
                # ����� ����� ��������� �������� ��������,
                #  ���� ������� ���������� �� ��������.
                for l in range(len(current)):
                    # ����������� ������ ���������� ��������.
                    if _compare((current[l], l+1), rectangle):
                        rectangle = (current[l], l+1)
                    # ����������� �������� �������� ������������
                    #  �� ��������� ��������.
            result[j][i] = (rectangle, colour)
            # � ������ ������������ ������������ ������� (������� 1�1),
            #  � ����� ��� ��� � ������� ����.
    return result
    # ������� ���������� ������� � ������������� ���������� ���������,
    #  ������������� �� ������ ������� �������� �����.

def count (matrix, mode='shallow'):
    '''
  ��� ����, ����� ����������, ����� �� ��� ������ ������������ �������
��� �����-���� ����� �����, ���������� �����, ���� �� ��� ��� ���-��.
������ ��� ������ ������ ������� count, �� � ���������� ����, ���
���������. � ���������, ��� ����� �� ������ ��������� ����������
��������� ���������, �� � �� ����� ���� �� �������������, ��� ����
����� ������������ ���� �������������.
    '''
    summ = 0
    for string in matrix:
        # ��� ������ ������ � �����...
        for item in string:
            # ...��� ������ ������ � ������...
            if item:
                # ...���� ��� ������ �� �����...
                if mode == 'shallow':
                    # ...������ ��������� ������.
                    summ += 1
                if mode == ('deep', 'plus'):
                    # ...�������� � ����� ����� ����� ���� ������.
                    subsum = 0
                    for sub in item:
                        if isinstance(sub, int): subsum += sub
                        if isinstance(sub, list): subsum += sub[0]
                        if isinstance(sub, tuple): subsum += sub[0]
                    summ += subsum
                if mode == ('deep', 'mult'):
                    # ...�������� � ����� ����� ��������� ������.
                    subsum = 1
                    for sub in item:
                        if isinstance(sub, int): subsum *= sub
                        if isinstance(sub, list): subsum *= sub[0]
                        if isinstance(sub, tuple): subsum *= sub[0]
                    summ += abs(subsum)
    '''
  ��� ���� ������� ������ ���� �����������. ��, �� �������
����, ��� ����� ��������� ���������, ����� �� ����� ������� ��������
����� ���� ��������� ����������� �����.
    '''
    #print(summ)
    return summ

def purge (matrix):
    '''
  ������ ������� �������� ��������. ��� �������� ��������������� �
�������� ������, �������� ���������� �� ��������� �������� � "������"
�������� �����, ������������ ���� ��������. ������ ��������� �����������
�� ��� ���, ���� ��� ������� ����� �� ���������.
    '''
    old = matrix
    # print count(old), 'elements in progress.'
    new = list()
    for j in range(len(old)):
        new.append(list())
        for i in range(len(old[j])):
            new[j].append((0, 0))
    # �������� ������� �������, �� ������� ����������� ��������
            
    while count(old):
        # ���� �������� �� ��� ���, ���� � ������� ������������ �������.
        current = cover(old)
        # �������� ���������� � ������� �������� ��� ������ ������ �����
        rectangle = (0, 0)
        # ���������������� ������� �������������.
        m, n = 0, 0
        for j in range(len(current)):
            for i in range(len(current[j])):
                if _compare(current[j][i][0], rectangle):
                    rectangle = current[j][i][0]
                    # ���� ������� ������� ������ ��������,
                    #  ��� �������� ��������.
                    m, n = i, j
                    # ���������� ����� ������� ������������.
        new[n][m] = (rectangle, current[n][m][1])
        # � ����� ��������� ������� ������������ ���������� �������.
        for j in range(rectangle[1]):
            for i in range(rectangle[0]):
                old[n+j][m+i] = 0
        # � �������� ���������� ������� �������� ����� ����������.
    return new
    # ������������ �������, � ������� ���������� ������ ������� �������,
    #  ���������� ������� � _�� ��������������_ ����� �����.

def make_dxf (matrix, px_size=1, center=(0, 0), layer='RASTER'):
    '''
  ��� ������� �� ��������, ������ ������� - ���� � ��������� dxf-����.
���� �� �� ������� � ����������� dxf-������, ������� �������� ��������
�� �������-������� �������, � �������-������� �����������,
� �������-���������� ����� � ������ ��������, � ����� - �������� ������:
https://github.com/DamTerrion/Lumenous/blob/nDXF/ndxf.py

  � ���� �� ����, �� � ������� ���� ��� ������.
���� �� ���� ������� ������ 'header' ��� 'end', �� ������� ����������
���� "���������" (������ ������ ��������), ���� ��������� �����.
���� �� �� ���� �������� ������� �����, �� ������������ ��� ���������,
�� ����� �� ������ �������.
    '''
    if isinstance(matrix, str):
        if matrix == 'header':
            return ['  0', 'SECTION',
                    '  2', 'ENTITIES']
        if matrix == 'end':
            return ['  0', 'ENDSEC',
                    '  0', 'EOF']
    counter = 0
    stack = []
    size = (px_size*len(matrix[0]),
            px_size*len(matrix))
    start = (center[0] - size[0]/2,
             center[1] + size[1]/2)
    # ������ �����, ������, �������� ������������� - ����� �����������
    stack.extend(['  0', 'POLYLINE',
                  '  8', str(layer)+'_b',
                  ' 66', '     1',
                  ' 40', '0.0',
                  ' 41', '0.0',
                  ' 70', '     1',
                  '  0', 'VERTEX',
                  '  8', str(layer)+'_b',
                  ' 10', str(start[0]),
                  ' 20', str(start[1]),
                  ' 30', '0.0',
                  '  0', 'VERTEX',
                  '  8', str(layer)+'_b',
                  ' 10', str(start[0]+size[0]),
                  ' 20', str(start[1]),
                  ' 30', '0.0',
                  '  0', 'VERTEX',
                  '  8', str(layer)+'_b',
                  ' 10', str(start[0]+size[0]),
                  ' 20', str(start[1]-size[1]),
                  ' 30', '0.0',
                  '  0', 'VERTEX',
                  '  8', str(layer)+'_b',
                  ' 10', str(start[0]),
                  ' 20', str(start[1]-size[1]),
                  ' 30', '0.0',
                  '  0', 'SEQEND',
                  '  8', str(layer)+'_b'])
    for j in range(len(matrix)):
        for i in range(len(matrix[j])):
            current = matrix[j][i][0]
            layer = matrix[j][i][1]
            if current and current != (0, 0):
                if current[1]%2:
                    y_shift = current[1]/2 + 0.5
                else:
                    y_shift = current[1]/2
                stack.extend([
                    '  0', 'POLYLINE',
                    '  8', str(layer),
                    ' 66', '      1',
                    ' 62', '{:>6}'.format(layer),
                    ' 40', str(current[1]*px_size),
                    ' 41', str(current[1]*px_size),
                    '  0', 'VERTEX',
                    '  8', str(layer),
                    ' 10', str(start[0] + px_size*( i           )),
                    ' 20', str(start[1] - px_size*( j + y_shift )),
                    ' 30', '0.0',
                    '  0', 'VERTEX',
                    '  8', str(layer),
                    ' 10', str(start[0] + px_size*( i+current[0])),
                    ' 20', str(start[1] - px_size*( j + y_shift )),
                    ' 30', '0.0',
                    '  0', 'SEQEND',
                    '  8', str(layer)
                    ])
                counter += 1
    return stack, counter
    # ������� ���������� ������ ����� ��� dxf-�����
    # ������ ����������� ����� �������������, �� � �������� ����

def split (img, size=(100, 100)):
    '''
  ������ ������� ������������� ��� ����, ����� ������ �����������
�� ��������� ���������. ������� ����������� �������������� �������
�����, ������� �� ����� ������ � ������������ �� ������.
    '''
    stack = []
    box = []
    border = (
        -img.size[0]/2,
        +img.size[1]/2
        )
    # ���������� border �������� ������� �����, ������ ��������� �����.
    if isinstance(size, int):
        size = (size, size)
    num = [
        img.size[0]//size[0]+1,
        img.size[1]//size[1]+1
        ]
    # ���������� num �������� ���������� ����������.
    residue = [
        img.size[0]%size[0],
        img.size[1]%size[1]
        ]
    # ���������� residue �������� ������ �������,
    #  �� �������� � ����� ���������.
    if residue[0] == 0:
        num[0] -= 1
        residue[0] = size[0]
    if residue[1] == 0:
        num[1] -= 1
        residue[1] = size[1]
    # ���� ������� ���, �� ���������� ���������� ������������ � �������,
    #  � �������� ��������� residue �� �������������� � ���������.
    box.extend(size)
    # ���������� box �������� ���������� ������ ���������,
    #  ������ ��� ���������, ������������� �� ������� ���� �����������
    #  ��������� ������� ����� ���� ������ ���� ���������.
    if num == (1, 1):
        return [(0, 0, img)]
    for j in range(num[1]):
        box[0] = size[0]
        if j == num[1]-1:
            box[1] = residue[1]
        for i in range(num[0]):
            if i == num[0]-1:
                box[0] = residue[0]
            x = (border[0]+i*size[0]+box[0]/2,
                 i*size[0],
                 i*size[0]+box[0])
            y = (border[1]-j*size[1]-box[1]/2,
                 j*size[1],
                 j*size[1]+box[1])
            stack.append((x[0], y[0], img.crop((x[1], y[1], x[2], y[2]))
                          ))
            # ����� img.crop() ���������� ����������� � ��������������,
            #  ���������� �������� ���������, ��� ������� � ����.
    return stack
    # ������� ���������� ������ ����������, �� ������� ���� ���������
    #  �������� �����������, ������ �� ������ ������������.

def test (img_name=False):
    '''
  ��� ������� ���������, ����� ��� ����������� ������ ��������
���������� ���������� ��������. ������� test ���������� ����������
�������� ��� ������� ���������� � ����������� �����.
  ����� �������: ���� 1 (�����) - �� �� �� �����, ��� � (255, 255, 255).
    '''
    if not img_name: img_name = input('Filename: ')
    img = Image.open(img_name+'.png')
    hist = dict()
    for j in range(img.size[1]):
        for i in range(img.size[0]):
            pixel = img.getpixel((i, j))
            px_name = str(pixel)
            if px_name in hist:
                hist[px_name] += 1
            else:
                hist[px_name] = 1
    for item in hist:
        print item, hist[item]

def do (filename=None,
        img_center=(0, 0),
        px_size=1,
        fragm_size=None
        ):
    '''
  ������ �������, �� ����, �������� �� �������, � ��������� ��� ������.
��� ��������� �����������, ����� ��� �� �����, ������������ ����������
��������� �� ������ ������ � ����� ������� �� � dxf-����.
    '''
    start_time = now()
    # ������ �� ����������� ����� ������ �������, � ��� ����� ���������
    #  �������� ��������� �������, ����� ������ ����������.
    lines_counter = 0
    # ���������� lines_counter ��������� ���������� ��������� ���������.
    dxf_body = []
    # ������������ ���� dxf-����� � ���� ������.
    if not filename: filename = input('Filename: ')
    img = Image.open(filename)
    # ���� ������� �������� ��� ����������, ������������ ��� �����
    #  ��� ���������. ����� ����������� png-���� � ���� ������.
    print ' '.join(('File', filename, 'loaded with',
                    str(img.size[0])+'x'+str(img.size[1]), 'px.'))
    # ����������� �� ���� ������ ��������� - ��� ������������.
    if fragm_size:
        # ���� ����� ������ ����������, ����������� ������� �� �����.
        splitted = split(img, fragm_size)
        if len(splitted) > 1:
            print 'Image was divided for', len(splitted), 'fragments.'
        fragm_num = 0
        for fragment in splitted:
            fragm_num += 1
            prepared, px_counter = mask(fragment[2])
            if px_counter[1] != 0:
                print px_counter[1], 'from', px_counter[0], 'px founded in fragment �', fragm_num
            #prepared = fragment[2].load()
            result = purge(prepared)
            dxf_fragm, addition = make_dxf(
                result, px_size,
                (fragment[0]*px_size + img_center[0],
                 fragment[1]*px_size + img_center[1]),
                filename)
            dxf_body.extend(dxf_fragm)
            # dxf-��� ������� �� ���������� ��������������� ������������
            #  � ����� ������ dxf-�����.
            lines_counter += addition
            # ������� ����� ������������� �� ������������ ����� �����.
    else:
        # ���� ������ �� �����, ����������� �������������� �������.
        prepared, px_counter = mask(img)
        print px_counter[1], 'from', px_counter[0], 'px founded in image.'
        result = purge(prepared)
        dxf_body, lines_counter = make_dxf(
            result, px_size, img_center, filename)
    
    dxf_head = make_dxf('header')
    dxf_end = make_dxf('end')
    dxf_text = '\n'.join(dxf_head +
                         dxf_body +
                         dxf_end)
    # �������� dxf-��� ���������� ���� "����������" ���� �����
    #  � ��������� � ���������.
    print lines_counter, 'polylines created.'
    output = open(filename+'.dxf', 'w')
    output.write(dxf_text)
    output.close()
    end_time = now()
    # dxf-��� ������������ � ���� � ������������ ����� ��������� ������.
    result_time = end_time - start_time
    if result_time >= 60:
        mins = result_time//60
        secs = result_time%60
        result_time = str(mins)+' m. '+str(secs)+' sec.'
    else: result_time = str(result_time)+' sec.'
    print 'File saved in', result_time
    log = open('masker.log', 'a')
    log.write(''.join((ctime(end_time),
                       '\t', filename,
                       '\t', 'fragms: ', str(fragm_size),
                       '\t', 'in ', result_time,
                       '\n'))
              )
    log.close()
    # ���������� � �������� � log-���� ������ �� �����������.

if __name__ == '__main__':
    do('CPPtest_70mm.bmp', (0, 0), 0.1367, (64, 64))
    #do('Craft1.png', (0, 0), 0.1367, (64, 64))
    pass
    '''
  ����� ������� ���� ����� ������� ����� ��������� � �����������,
����� ��� ���� ���������� ����� ����� ������� �������. ��� �������� ��
��� ���� � ������� ������� do() � ��������� ������ �������.
    '''
