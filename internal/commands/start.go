package commands

import (
	"EverythingSuckz/fsb/config"
	"EverythingSuckz/fsb/internal/utils"

	"github.com/celestix/gotgproto/dispatcher"
	"github.com/celestix/gotgproto/dispatcher/handlers"
	"github.com/celestix/gotgproto/ext"
	"github.com/celestix/gotgproto/storage"
	"github.com/gotd/td/tg"
)

func (m *command) LoadStart(dispatcher dispatcher.Dispatcher) {
	log := m.log.Named("start")
	defer log.Sugar().Info("Loaded")
	dispatcher.AddHandler(handlers.NewCommand("start", start))
}

func start(ctx *ext.Context, u *ext.Update) error {
	chatId := u.EffectiveChat().GetID()
	peerChatId := ctx.PeerStorage.GetPeerById(chatId)
	if peerChatId.Type != int(storage.TypeUser) {
		return dispatcher.EndGroups
	}
	replyMarkup := &tg.ReplyInlineMarkup{
			Rows: []tg.KeyboardButtonRow{
				{
					Buttons: []tg.KeyboardButtonClass{
						&tg.KeyboardButtonURL{
							Text: "Support Groups!",
							URL:  "https://t.me/+2u67mVOGziU5YzRh",
						},
						&tg.KeyboardButtonURL{
							Text: "Join Channel!",
							URL:  "https://kai_verse.t.me",
						},
					},
				},
			},
		}
	opts := &ext.ReplyOpts{Markup: replyMarkup}
	if len(config.ValueOf.AllowedUsers) != 0 && !utils.Contains(config.ValueOf.AllowedUsers, chatId) {
		
		ctx.Reply(u, "You are not allowed to use this bot.", opts)
		return dispatcher.EndGroups
	}
	ctx.Reply(u, "Hi, send me any file to get a direct streamable link to that file.", opts)
	return dispatcher.EndGroups
}
