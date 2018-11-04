from none import on_request, RequestSession, on_command, CommandSession
import plugins.getUser

@on_request('friend')
async def _(session: RequestSession):
    await session.approve()
    return

@on_request('group')
async def _(session: RequestSession):
    await session.approve()
    return

@on_command('help',only_to_me=False)
async def _(session: CommandSession):
    print(session.ctx)
    await session.send("您好，欢迎使用himikochan机器人。\n这bot就俩功能，订阅看实时飞图状态和取消订阅，订阅!subscribe/!sub/!s，取消订阅!unsubscribe/!unsub/!u，谢谢合作。\n有问题请联系QQ: 397158185/OSU: Yumeno Himiko。")

@on_command('subscribe',aliases=('sub','s'),only_to_me=False)
async def _(session: CommandSession):
    list = plugins.getUser.getUsers()

    if session.ctx['message_type'] == 'private' and session.ctx['user_id'] in list['user']:
        await session.send('您已经订阅！')
        return

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']:
        await session.send('本群已经订阅！')
        return

    if session.ctx['message_type'] == 'private' and session.ctx['user_id'] not in list['user']:
        list['user'].append(session.ctx['user_id'])
        await session.send('订阅成功！')
        plugins.getUser.saveUsers(list)

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']:
        list['group'].append(session.ctx['group_id'])
        await session.send('订阅成功！')
        plugins.getUser.saveUsers(list)

@on_command('unsubscribe',aliases=('unsub','u'),only_to_me=False)
async def _(session: CommandSession):
    list = plugins.getUser.getUsers()

    if session.ctx['message_type'] == 'private' and session.ctx['user_id'] not in list['user']:
        await session.send("您已不在订阅！")
        return

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']:
        await session.send("本群已不在订阅！")
        return

    if session.ctx['message_type'] == 'private' and session.ctx['user_id'] in list['user']:
        list['user'].remove(session.ctx['user_id'])
        await session.send('已取消订阅！')
        plugins.getUser.saveUsers(list)

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']:
        list['group'].remove(session.ctx['group_id'])
        await session.send('已取消订阅！')
        plugins.getUser.saveUsers(list)
