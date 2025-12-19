import urllib.request
import wx
import wx.media


#Adding logo to the app
def img(url):
    img1=urllib.request.urlopen(url).read()
    from io import BytesIO
    img2=BytesIO(img1)
    img3=wx.Image(img2,wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    return img3


#Play and Pause the theme music
def pm(e):
    global tf
    if tf:
        m.Stop()
        mb.SetLabel("🔇")
        tf=False
    else:
        m.Play()
        mb.SetLabel("🔈")
        tf=True


def magic_square_odd(n):
    magic = [[0]*n for _ in range(n)]
    i, j = 0, n//2

    for num in range(1, n*n + 1):
        magic[i][j] = num
        new_i = (i - 1) % n
        new_j = (j + 1) % n

        if magic[new_i][new_j] != 0:
            i = (i + 1) % n
        else:
            i, j = new_i, new_j

    return magic


def magic_square_doubly_even(n):
    magic = [[(i*n) + j + 1 for j in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(n):
            if (i % 4 == j % 4) or ((i+j) % 4 == 3):
                magic[i][j] = n*n + 1 - magic[i][j]

    return magic


def magic_square_singly_even(n):
    half = n//2
    sub_square = magic_square_odd(half)
    magic = [[0]*n for _ in range(n)]
    add = [0, 2*half*half, 3*half*half, half*half]

    idx = 0
    for r in range(2):
        for c in range(2):
            for i in range(half):
                for j in range(half):
                    magic[i + r*half][j + c*half] = sub_square[i][j] + add[idx]
            idx += 1

    k = (n - 2) // 4
    for i in range(n):
        for j in range(n):
            if i < half:
                if j < k or j >= n-k and j < n:
                    if j == 0 and i == half//2:
                        continue
                    temp = magic[i][j]
                    magic[i][j] = magic[i + half][j]
                    magic[i + half][j] = temp

    return magic


def md():
    app2=wx.App()
    frame2=wx.Frame(None,title="Magic Square Generator",size=(500,500))
    panel2=wx.Panel(frame2)
    panel2.SetBackgroundColour("#A360DF")
    m=wx.MessageDialog(panel2,"Magic Square for the given sum can't be generated","Error",wx.OK|wx.ICON_ERROR)
    if m.ShowModal()==wx.ID_OK:
        e=wx.TextEntryDialog(panel2,"Enter your target sum:","Target Sum","0")
        e.SetBackgroundColour("#A360DF")
        if e.ShowModal()==wx.ID_OK:
            ts=int(e.GetValue())
            e.Destroy()
            generate(ts,panel2)
        else:
            frame2.Close()
    frame2.Show()
    app2.MainLoop()


#To find dimensions
def find_valid_order(target_sum):
    n = 3
    while True:
        M = n * (n*n + 1) // 2
        if M>target_sum:
            md()
        if target_sum % M == 0:
            return n, target_sum // M
        n += 1


#Generating Magic Square
def generate(target_sum,panel):
    n, scale = find_valid_order(target_sum)
    st=wx.StaticText(panel,label=f"Generating a {n} × {n} magic square...",pos=(10,20))
    st.SetFont(wx.Font(16,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_SLANT,wx.FONTWEIGHT_BOLD))
    s=wx.StaticText(panel,label=f"\nEach row, column and diagonal sums to: {target_sum}",pos=(10,45))
    s.SetFont(wx.Font(14,wx.FONTFAMILY_DECORATIVE,wx.FONTSTYLE_SLANT,wx.FONTWEIGHT_SEMIBOLD))
    if n % 2 == 1:
        square = magic_square_odd(n)
    elif n % 4 == 0:
        square = magic_square_doubly_even(n)
    else:
        square = magic_square_singly_even(n)
    # Scale the square
    fs = [[square[i][j] * scale for j in range(n)] for i in range(n)]
    formation(fs,n,panel)


#Display
def formation(fs,n,panel):
    h,v=10,105
    l=0
    if n==4:
        l=(10*(n+1)-1)+(n-3)-(n*2)-2
    elif n==6:
        l=(10*(n+1)-1)+(n-3)-(n*2)
    else:
        l=(10*(n+1)-1)+(n-3)-(n*2)-6+n
    w1=wx.StaticText(panel,label='-'*l,pos=(h,v))
    for i in fs:
        v+=10
        h=10
        b=wx.StaticText(panel,label='|',pos=(h,v))
        for j in i:
            cw1=wx.StaticText(panel,label=str(j).center(13),pos=((h+3),v))
            h+=50
            cw2=wx.StaticText(panel,label='|',pos=((h+3),v))
        h=10
        v+=15
        w2=wx.StaticText(panel,label='-'*l,pos=(h,v))


# MAIN PROGRAM
def main():
    app1=wx.App()
    frame1=wx.Frame(None,title="Magic Square Generator",size=(500,500))
    panel1=wx.Panel(frame1)
    panel1.SetBackgroundColour("#A360DF")
    d=wx.TextEntryDialog(panel1,"Enter your target sum:","Target Sum","0")
    d.SetBackgroundColour("#A360DF")
    if d.ShowModal()==wx.ID_OK:
        ts=int(d.GetValue())
        d.Destroy()
        generate(ts,panel1)
    else:
        frame1.Close()
    frame1.Show()
    app1.MainLoop()


#when start button is clicked
def sb(e):
    main()


#when "how it works?" button is clicked
def hb(e):
    d=wx.MessageDialog(panel,"A magic square is an nXn grid of distinct integers where, Sum of rows=Sum of columns=Sum of right diagonal=Sum of left diagonal","Info",wx.OK|wx.ICON_INFORMATION)
    d.ShowModal()
    d.Destroy()


#front page
app=wx.App()
frame=wx.Frame(None,title="Magic Square Generator",size=(700,700))
panel=wx.Panel(frame)
panel.SetBackgroundColour("#A360DF")
sizer=wx.BoxSizer(wx.VERTICAL)
s=wx.StaticText(panel,label="Magic Square Generator")
s.SetFont(wx.Font(20,wx.FONTFAMILY_SCRIPT,wx.FONTSTYLE_MAX,wx.FONTWEIGHT_EXTRAHEAVY))
imagefile="https://i.postimg.cc/mkJ3PQCx/IMG-20251129-WA0011.jpg"
bm=img(imagefile)
b=wx.BitmapButton(panel,bitmap=bm,size=(298,304))
musicfile="https://files.catbox.moe/1lsp23.mp3"
tf=True
m=wx.media.MediaCtrl(panel)
mm=m.LoadURI(musicfile)
m.Play()
mb=wx.Button(panel,label="🔈")
mb.Bind(wx.EVT_BUTTON,pm)
b1=wx.Button(panel,label="Start")
b1.Bind(wx.EVT_BUTTON,sb)
b2=wx.Button(panel,label="How it works?")
b2.Bind(wx.EVT_BUTTON,hb)
sizer.Add(s,1,wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL,50)
sizer.Add(b,1,wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL,10)
sizer.Add(b1,1,wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL,10)
sizer.Add(b2,1,wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL,5)
sizer.Add(mb,1,wx.ALL|wx.ALIGN_LEFT,10)
panel.SetSizer(sizer)
frame.Show()
app.MainLoop()
