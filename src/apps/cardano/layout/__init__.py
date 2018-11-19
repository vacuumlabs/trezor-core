from micropython import const

from trezor import ui
from trezor.messages import ButtonRequestType, MessageType
from trezor.messages.ButtonRequest import ButtonRequest
from trezor.ui.confirm import CONFIRMED, ConfirmDialog, HoldToConfirmDialog
from trezor.ui.scroll import Scrollpage, animate_swipe, paginate
from trezor.ui.text import Text
from trezor.utils import chunks, format_amount

def format_coin_amount(amount, coin):
    return "%s %s" % (format_amount(amount, 6), coin)


async def confirm_sending(ctx, amount, to, coin):
    to_lines = list(chunks(to, 17))

    t1 = Text("Confirm transaction", ui.ICON_SEND, icon_color=ui.GREEN)
    t1.normal("Confirm sending:")
    t1.bold(format_coin_amount(amount, coin))
    t1.normal("to:")
    t1.bold(to_lines[0])
    pages = [t1]

    LINES_PER_PAGE = 4
    if len(to_lines) > 1:
        to_pages = list(chunks(to_lines[1:], LINES_PER_PAGE))
        for page in to_pages:
            t = Text("Confirm transaction", ui.ICON_SEND, icon_color=ui.GREEN)
            for line in page:
                t.bold(line)
            pages.append(t)

    paginator = paginate(create_renderer(ConfirmDialog), len(pages), const(0), pages)
    return await ctx.wait(paginator) == CONFIRMED
    return True


async def confirm_transaction(ctx, amount, fee, coin):
    t1 = Text("Confirm transaction", ui.ICON_SEND, icon_color=ui.GREEN)
    t1.normal("Total amount:")
    t1.bold(format_coin_amount(amount, coin))
    t1.normal("including fee:")
    t1.bold(format_coin_amount(fee, coin))

    pages = [t1]
    paginator = paginate(create_renderer(HoldToConfirmDialog), len(pages), const(0), pages)
    return await ctx.wait(paginator) == CONFIRMED


def create_renderer(confirmation_wrapper):
    @ui.layout
    async def page_renderer(page: int, page_count: int, pages: list):
        # for som reason page index can be equal to page count
        if page >= page_count:
            page = page_count - 1

        content = Scrollpage(pages[page], page, page_count)
        if page + 1 >= page_count:
            return await confirmation_wrapper(content)
        else:
            content.render()
            await animate_swipe()
    return page_renderer
